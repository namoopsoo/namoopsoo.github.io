---
title: Nice pretty printing go slices
date: 2024-03-30
---


```go
package main

import (
	"encoding/json"
	"fmt"
)

type Foo struct {
	Blah  int
	Flarg string
}

func main() {
	var stuff []Foo = []Foo{
		Foo{Blah: 8, Flarg: "sure"},
		Foo{Blah: 7, Flarg: "mhm"},
	}
	stuffBytes, err := json.MarshalIndent(stuff, "", " ")
	if err != nil {
		fmt.Println("Marshaling errors", err)
		return
	}
	fmt.Println("harder to read\n", stuff)

	fmt.Println("\nbetter\n", string(stuffBytes))

}

```
outupt is easy on the eyes 

```
harder to read
 [{8 sure} {7 mhm}]

better
 [
 {
  "Blah": 8,
  "Flarg": "sure"
 },
 {
  "Blah": 7,
  "Flarg": "mhm"
 }
]
```
