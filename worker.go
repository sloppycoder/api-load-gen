package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync/atomic"
	"time"

	"github.com/google/uuid"
	"github.com/myzhan/boomer"
)

var client *http.Client
var total, failed uint64 = 0, 0
var verbose, useRandomID, v2 = false, false, false
var baseURL, testDataFile string
var sleep int
var entries [][]string = [][]string{{"GRP1", "01", "20210530"}}

func initTestData() {
	if useRandomID {
		return
	}

	dataFile := testDataFile
	if dataFile == "" {
		dataFile = "dummy_data.csv"
	}

	if _, err := os.Stat(dataFile); os.IsNotExist(err) {
		log.Printf("Invalid test data file %s", dataFile)
		return
	}

	file, err := os.Open(dataFile)
	if err != nil {
		log.Printf("Cannot open test data file %s", dataFile)
		return
	}
	defer file.Close()

	r := csv.NewReader(file)
	entries, err := r.ReadAll()
	if err != nil {
		log.Printf("Error when reading CSV file %s", dataFile)
		return
	}

	// randomize the order by shuffle it 3 times
	if len(entries) > 5 {
		for i := 0; i < 3; i++ {
			rand.Shuffle(len(entries), func(i, j int) { entries[i], entries[j] = entries[j], entries[i] })
		}
	}

	log.Printf("iniatialized test data from %s", dataFile)
}

func nextEntry() (map[string]string, error) {
	if useRandomID {
		return map[string]string{
			"GroupId":   "GRP1111",
			"AccountNo": "random",
			"asOf":      "",
		}, nil
	}

	entry := entries[rand.Intn(len(entries))] //nolint:gosec
	if len(entry) < 3 {
		return nil, fmt.Errorf("invalid test data %v", entry)
	}

	return map[string]string{
		"GroupId":   entry[0],
		"AccountNo": entry[1],
		"asOf":      entry[2],
	}, nil
}

func apiURL(accountNum string) string {
	base := "/accounts/"
	if v2 {
		base += "v2/"
	}
	if useRandomID {
		return base + "random"
	}
	return base + accountNum
}

func readAndDiscard(response *http.Response) {
	_, _ = io.Copy(ioutil.Discard, response.Body)
	_ = response.Body.Close()
}

func invokeAPI() {
	params, err := nextEntry()
	if err != nil {
		log.Printf("%v", err)
		return
	}

	path := apiURL(params["AccountNo"])
	request, err := http.NewRequest("GET", baseURL+path, nil)
	if err != nil {
		log.Fatalf("%v\n", err)
	}

	id, _ := uuid.NewRandom()
	request.Header.Set("CorrelationId", id.String())
	request.Header.Set("GroupId", params["GroupId"])
	request.Header.Set("Accept", "application/json")

	startTime := time.Now()
	response, err := client.Do(request)
	elapsed := time.Since(startTime)

	atomic.AddUint64(&total, 1)

	switch {
	case err != nil:
		if verbose {
			log.Printf("%v\n", err)
		}
		chunks := strings.Split(err.Error(), ":")
		errMsg := chunks[len(chunks)-1]
		boomer.RecordFailure("GET", path, 0.0, errMsg)

		atomic.AddUint64(&failed, 1)
	case response.StatusCode != 200:
		errMsg := "statusCode=" + strconv.Itoa(response.StatusCode)
		boomer.RecordFailure("GET", path, 0.0, errMsg)

		readAndDiscard(response)

		atomic.AddUint64(&failed, 1)
	default:
		boomer.RecordSuccess("GET", path,
			elapsed.Nanoseconds()/int64(time.Millisecond), response.ContentLength)

		readAndDiscard(response)
	}

	if sleep > 0 {
		time.Sleep(time.Duration(sleep) * time.Millisecond)
	}
}

func initHTTPClient() {
	http.DefaultTransport.(*http.Transport).MaxIdleConnsPerHost = 2000
	tr := &http.Transport{
		MaxIdleConnsPerHost: 10,
		DisableCompression:  true,
		DisableKeepAlives:   false,
	}
	client = &http.Client{
		Transport: tr,
		Timeout:   time.Duration(10) * time.Second,
	}
}

func main() {
	flag.StringVar(&baseURL, "host", "http://accounts:8080", "base URL for endpoint to call")
	flag.StringVar(&testDataFile, "data", "", "CSV file that contains test data")
	flag.IntVar(&sleep, "sleep", 0, "sleep between each request in ms")
	flag.BoolVar(&useRandomID, "random-id", false, "Use random as account number in request")
	flag.BoolVar(&verbose, "verbose", false, "Print debug log")
	flag.BoolVar(&v2, "v2", false, "Use v2 in request url")
	flag.Parse()

	if !strings.HasSuffix(baseURL, "/") {
		baseURL += "/"
	}

	log.Printf("API endpoint is %s, random-id=%t, sleep=%d", baseURL, useRandomID, sleep)

	rand.Seed(time.Now().UnixNano())
	initTestData()
	initHTTPClient()

	task1 := &boomer.Task{
		Name:   "invoke_api",
		Weight: 10,
		Fn:     invokeAPI,
	}

	boomer.Run(task1)
}
