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



```go
```


