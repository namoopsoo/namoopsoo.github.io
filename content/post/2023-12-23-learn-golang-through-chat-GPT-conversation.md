---
title: Some of my notes through learning Golang by conversing with ChatGPT
date: 2023-12-23
---

## I have not messed around with Golang yet and figured why not try to learn this through just chatting with ChatGPT? 

Not a full conversation below , but just using this to jot down some notes. And most of the code examples I'm pasting below are from ChatGPT.


## Error handling is very different in Go
So no exceptions like Python. Instead, you can give a return tuple type from a function like this and the second term will be a error code.


```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10.0, 0)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)
}

```

## Attaching functions to struct types 
So there are no classes per se. You can however attach methods to structs, with this additional syntactic sugar, below. 

There is an additional `(r Rectangle)` squished in between `func` and `Area` and the arguments are an empty `()`. 

In addition , an interface is defined also below, `Shape`, which carries a subset of the methods that are defined on the struct type `Rectangle`.

```go
package main

import "fmt"

// Define a struct
type Rectangle struct {
    Width, Height float64
}

// Define a method on the struct
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// Define an interface
type Shape interface {
    Area() float64
}

func main() {
    var s Shape = Rectangle{Width: 10, Height: 5}
    fmt.Println("Area:", s.Area())
}
```

In addition, I was inquiring in the above , why bother specifying that the return of `Area` in the interface `Shape` is `float64` if we already know the type from the earlier definition of `Area` earlier. And the response was that more or less the interface is a contract and that types "might" implement  it or they might not. 

### Indeed, I tried changing the return type to see what would happen
So only updating that one thing, I tried running the below in https://go.dev/play/ 
```go
package main

import "fmt"

// Define a struct
type Rectangle struct {
	Width, Height float64
}

// Define a method on the struct
func (r Rectangle) Area() int {
	return r.Width * r.Height
}

// Define an interface
type Shape interface {
	Area() float64
}

func main() {
	var s Shape = Rectangle{Width: 10, Height: 5}
	fmt.Println("Area:", s.Area())
}
```

and actually first I got a message that multiplying floats will not produce an `int`. Very nice.
```
./prog.go:12:9: cannot use r.Width * r.Height (value of type float64) as int value in return statement
```
And I also got the message, 

```
./prog.go:21:16: cannot use Rectangle{…} (value of type Rectangle) as Shape value in variable declaration: Rectangle does not implement Shape (wrong type for method Area)
		have Area() int
		want Area() float64
```
and the line 21 above is the `var s Shape = Rectangle{Width: 10, Height: 5}` , so, cool, as expected, this is an error not on the interface, not on the type implementing the interface, but on the declaration that attempts to use the type `Rectangle` claiming to implement the interface `Shape`. Interesting.

And indeed when I fix the types of `Width` and `Height` to `int` in `Rectangle` and comment out that line `21` above, the program actually has no compile error, so then looks like this is a runtime error only.

## Behavior of passing objects into functions
Ok, we have pass by value behavior and we have pass by reference behavior, depending on the type. 

Wow, i learned that the size of a Go array is part of its type and therefore you must define a different function for different sizes of arrays as inputs. 

But this is not true of slices as function parameters, which   also have a pass by reference behavior as opposed to array pass by value behavior and so overall seems like passing slices to functions is the way to go.

```go
```

## HTTP server with channels for delegating to  workers

Discussing this, I was asking , hey if I want to build a web server with Golang, with a listener that receives HTTP requests and then pushes them to channels for available workers to consume , are channels good option for this or would this cause the listener go routine to block on channel push operations? 

Chat GPT reminding me that, unbufferes channels block but also buffered channels that are "full" also block. 

But the recommendation was to use a channel with a capacity that is large enough to handle peak loads, and then that would prevent a listener from blocking on a push to the channel.

Yea good point!

### Received this example code based on my question


```go
package main

import (
    "fmt"
    "net/http"
    "time"
)

func worker(id int, jobs <-chan http.Request) {
    for req := range jobs {
        fmt.Printf("Worker %d processing request: %v\n", id, req)
        // Process the request...
    }
}

func main() {
    jobs := make(chan http.Request, 100) // Buffered channel

    // Start worker goroutines
    for w := 1; w <= 3; w++ {
        go worker(w, jobs)
    }

    // HTTP listener (simplified example)
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("Received request:", r)
        jobs <- *r // Send the request to the channel
        fmt.Fprintln(w, "Request is being processed")
    })

    http.ListenAndServe(":8080", nil)
}

```
Nice let me see if it runs  !

### Okay that basically worked out of the box
Only that `"time"` was imported but unused. Other than that worked like here, after putting this into a `serve.go`

```sh
go run serve.go
```
and I used a python repl to call the server, 
```python
import requests

In [2]: data = {"some": "data"}
   ...: r = requests.post("http://localhost:8080", json=data)

In [3]: r.status_code, r.text
Out[3]: (200, 'Request is being processed\n')

```
And saw this in my STDOUT logs, 
```sh
Received request: &{POST / HTTP/1.1 1 1 map[Accept:[*/*] Accept-Encoding:[gzip, deflate] Connection:[keep-alive] Content-Length:[16] Content-Type:[application/json] User-Agent:[python-requests/2.31.0]] 0xc00012a240 <nil> 16 [] false localhost:8080 map[] map[] <nil> map[] 127.0.0.1:63359 / <nil> <nil> <nil> 0xc000076230}
Worker 1 processing request: {POST / HTTP/1.1 1 1 map[Accept:[*/*] Accept-Encoding:[gzip, deflate] Connection:[keep-alive] Content-Length:[16] Content-Type:[application/json] User-Agent:[python-requests/2.31.0]] 0xc00012a240 <nil> 16 [] false localhost:8080 map[] map[] <nil> map[] 127.0.0.1:63359 / <nil> <nil> <nil> 0xc000076230}

```
Nice, so the response is provided by the server, `Request is being processed`. And a cool next step would be, okay probably I should pass the response writer `http.ResponseWriter` to the worker, so that it can send the response? Let me try. 

### First try produced empty responses for the client
So I created a new struct type, for both the request and the response writer, 
```go

type Packet struct {
    request http.Request
    response_writer http.ResponseWriter
}
```
And I was passing this to the worker through the channel, 
```go
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("Received request:", r)
        done := make(chan struct{})
        packet := Packet{
            request: *r, response_writer: w,
            }
        jobs <- packet // Send the request to the channel
    })
```
with worker , like 
```go
func worker(id int, jobs <-chan Packet) {
    for packet := range jobs {
        req := packet.request
        response_writer := packet.response_writer
        fmt.Printf("Worker %d processing request: %v\n", id, req)

        // Process the request...
        fmt.Fprintln(response_writer, "Request is being processed")
    }
}
```
So when the response on the client was blank, this was puzzling. I inquired w/ ChatGPT and got the idea that oh wow 😮right, the listener is likely returning a response before the worker writes to the buffer there. So I should have the handler block until the worker is done by using a per request channel, `done`. 

### Ok, so I tried creating adding a channel on which the handler blocks and that worked !

```go

package main

import (
    "fmt"
    "net/http"
    // "time"
)


type Packet struct {
    request http.Request
    response_writer http.ResponseWriter
    done chan struct{}
}

func worker(id int, jobs <-chan Packet) {
    for packet := range jobs {
        req := packet.request
        response_writer := packet.response_writer
        fmt.Printf("Worker %d processing request: %v\n", id, req)


        // Process the request...
        fmt.Fprintln(response_writer, "Request is being processed")

        // Signal we are done 
        packet.done <- struct{}{}
    }
}

func main() {
    fmt.Println("Server has started.")
    jobs := make(chan Packet, 100) // Buffered channel

    // Start worker goroutines
    for w := 1; w <= 3; w++ {
        go worker(w, jobs)
    }

    // HTTP listener (simplified example)
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("Received request:", r)
        done := make(chan struct{})
        packet := Packet{
            request: *r, response_writer: w, done: done,
            }
        jobs <- packet // Send the request to the channel
        <- done
    })

    http.ListenAndServe(":8080", nil)
}
```
And on client side, 
```go
In [10]: data = {"some": "xxxxxxxxxxxxxxxxxxxx"}
    ...: r = requests.post("http://localhost:8080", json=data)
    ...: r.status_code, r.text
Out[10]: (200, 'Request is being processed\n')
```
Nice. 

