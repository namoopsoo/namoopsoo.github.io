---

title: "Scope trickiness in Go"

date: 2024-03-30
---


## Go scope is different for for loops and if blocks than in Python

For example, with some code,

```go

package main

import (
	"fmt"
	"slices"
)

func main() {
	var stuff = []string{
		"foo", "bar", "hmm",
	}

	if idx := slices.IndexFunc(stuff, func(x string) bool { return x == "foo" }); idx == -1 {
		fmt.Println("yes")
		found := true
	} else {
		fmt.Println("no")
		found := false
	}
	fmt.Printf("found %v\n", found)

}

```

But the error is 
```
./prog.go:17:3: found declared and not used
./prog.go:20:3: found declared and not used
./prog.go:22:27: undefined: found
```


### Instead just need to define found outside the


```go
package main

import (
"fmt"
"slices"
)

func main() {
var stuff = []string{
    "foo", "bar", "hmm",
}
found := false

if idx := slices.IndexFunc(stuff, func(x string) bool { return x == "foo" }); idx == -1 {
    fmt.Println("yes")
    found = true
} else {
    fmt.Println("no")
    found = false
}
fmt.Printf("found %v\n", found)

}
```

And get

```
no
found false
```
