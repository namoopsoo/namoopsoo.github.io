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

```go
```


