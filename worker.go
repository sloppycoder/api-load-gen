package main

import (
	"flag"
	"io"
	"io/ioutil"
	"log"
	"net/http"
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
var baseURL string
var sleep int

func nextParams() (string, string) {
	return "GRP1111", "11223344"
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
	io.Copy(ioutil.Discard, response.Body)
	response.Body.Close()
}

func invokeAPI() {
	groupID, accNum := nextParams()
	path := apiURL(accNum)

	request, err := http.NewRequest("GET", baseURL+path, nil)
	if err != nil {
		log.Fatalf("%v\n", err)
	}

	id, _ := uuid.NewRandom()
	request.Header.Set("CorrelationId", id.String())
	request.Header.Set("GroupId", groupID)
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
	flag.IntVar(&sleep, "sleep", 0, "sleep between each request in ms")
	flag.BoolVar(&useRandomID, "random-id", true, "Use random as account number in request")
	flag.BoolVar(&verbose, "verbose", false, "Print debug log")
	flag.BoolVar(&v2, "v2", false, "Use v2 in request url")
	flag.Parse()

	if !strings.HasSuffix(baseURL, "/") {
		baseURL += "/"
	}

	log.Printf("API endpoint is %s, random-id=%t, sleep=%d", baseURL, useRandomID, sleep)

	initHTTPClient()

	task1 := &boomer.Task{
		Name:   "invoke_api",
		Weight: 10,
		Fn:     invokeAPI,
	}

	boomer.Run(task1)
}
