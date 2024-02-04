



## Asked chat gpt the following conundrum, 

 if I'm using Go struct types to model a data type, matching a table in my postgresql database say, 

```
type Merchant struct {
    id int,
    created_at time.Time,
    name string,
    phone string,
    email string,
}
```
I have the following question, does it make sense that I ended up creating different types also for the HTTP request to create this merchant, 


```
type CreateMerchantRequest struct {
    name string,
    phone string,
    email string,
}
```
since the `id` and `created_at` timestamps are populated automatically, 
and also another to update the merchant,

```
type UpdateMerchantRequest struct {
    id int,
    name string,
    phone string,
    email string,
}
```
since my request does need the `id` and any fields that need updating,

yet now is the question, that what if an update only applies to one field, does that mean now we need yet another kind of type? 

```
type UpdatePhoneMerchantRequest struct {
    id int,
    phone string,
}
```
? 
Is this getting out of hand? Am I on the right track? What is a more "dont repeat yourself" pattern here ?


## Got a cool response, learned about `omitempty` ! 

> Your approach to creating distinct Go struct types for different operations (like creating and updating a merchant) is quite common and reasonable in many application designs. It helps to clearly define what data is required for each operation, enhancing code readability and safety. However, as you've noticed, it can lead to a proliferation of types, especially for operations that only update a part of the model. Here are some strategies to manage this complexity:

### And here is the idea on using pointers for optional fields, 
So the below, code snippet haha also has the fields title-cased because I forgot to do that.  And yea I will try this out but I think it means a partially filled json request can still be unmarshalled into the same dont-repeat-yourself type, `UpdateMerchantRequest`.


```go
Copy code
type UpdateMerchantRequest struct {
    ID    *int    `json:"id"`
    Name  *string `json:"name,omitempty"`
    Phone *string `json:"phone,omitempty"`
    Email *string `json:"email,omitempty"`
}
```

> In this model, a field set to nil means it was not included in the update request and should not be changed. This approach minimizes the number of structs you need and allows for flexible updates.

