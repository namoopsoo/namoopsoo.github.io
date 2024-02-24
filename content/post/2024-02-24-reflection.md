---
title: Go Sprinkle reflection on domain driven development
date: 2024-02-24
---



Ok cool, realizing, following on from earlier post, that to nicely test the case when I have a `Merchant` and I am only making updates to it with `UpdateMerchantRequest`, I would need a nice generic way to obtain a subset struct instance from the other. Getting ChatGPT to help, here is what I asked, 


> Okay I have a strategy I'm using, where I have a go struct for a merchant that mirrors a postgresql database table and also another struct for updates to it which is a subset, 

```
import "time"
struct Merchant {
    Id int
    Name string
    CreatedAt time.Time()
    UpdatedAt time.Time()
}
struct UpdateMerchant {
    Id int
    Name string
}
```
> I want to be able to easily take an instance of Merchant and convert it into UpdateMerchant.
> But this is not an isolated example so I don't want to create a one-off function to do this manually.

> I might have similarly, `Customer` and `UpdateCustomer`, etc. the `Update` struct  always contains  a subset of fields. 

> Is there a canonical way to handle this in Go, taking an instance of the super struct and creating the subset struct ?

### And got back the idea of using reflection
Just the code from the response. Works out of the box.
```
package main

import (
    "fmt"
    "reflect"
    "time"
)

type Merchant struct {
    Id        int
    Name      string
    CreatedAt time.Time
    UpdatedAt time.Time
}

type UpdateMerchant struct {
    Id   int
    Name string
}

// CopyCommonFields copies fields from src to dst struct where fields are common.
// Both src and dst must be pointers to structs.
func CopyCommonFields(src, dst any) {
    srcVal := reflect.ValueOf(src).Elem()
    dstVal := reflect.ValueOf(dst).Elem()

    for i := 0; i < dstVal.NumField(); i++ {
        dstField := dstVal.Field(i)
        srcField := srcVal.FieldByName(dstVal.Type().Field(i).Name)

        if srcField.IsValid() && srcField.Type() == dstField.Type() {
            dstField.Set(srcField)
        }
    }
}

func main() {
    merchant := Merchant{
        Id:        1,
        Name:      "Example Merchant",
        CreatedAt: time.Now(),
        UpdatedAt: time.Now(),
    }

    updateMerchant := UpdateMerchant{}
    CopyCommonFields(&merchant, &updateMerchant)

    fmt.Printf("Original Merchant: %+v\n", merchant)
    fmt.Printf("Update Merchant: %+v\n", updateMerchant)
}

```
