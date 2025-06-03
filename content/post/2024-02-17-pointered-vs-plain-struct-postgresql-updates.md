









```go
// update table depending on what update fields are not nil
func UpdateEntityNonNil[T any](tableName string, request T, dryRun bool) error {
	v := reflect.ValueOf(request)

	var setClauses []string
	var args []interface{}
	for i := 0; i < v.NumField(); i++ {
		field := v.Field(i)
		jsonTag := v.Type().Field(i).Tag.Get("json")
		if jsonTag == "id" {
			args = append([]interface{}{field.Interface()}, args...) // Prepend ID to args for WHERE clause
		}
		if field.Kind() == reflect.Ptr && !field.IsNil() {
			jsonTag := v.Type().Field(i).Tag.Get("json")
			// For PostgreSQL, use $n placeholders
			setClauses = append(setClauses, fmt.Sprintf("%s = $%d", jsonTag, len(args)+1))
			args = append(args, field.Elem().Interface())
		}
	}

	// Assuming the ID field exists and is the first field
	if len(args) == 0 {
		return fmt.Errorf("no fields to update")
	}

	// Construct and execute the SQL statement
	sql := fmt.Sprintf("update %s set %s where id = $1", tableName, strings.Join(setClauses, ", "))
	fmt.Printf("\n\nUpdteEntity: sql: %q, args: %v", sql, args)
	if dryRun == true {
		fmt.Printf("\n\ndry run no update!")
		return nil
	} else {
		_, err := Conn.Exec(context.Background(), sql, args...)
		return err
	}
}


```


```go
func UpdateEntity [T any](tableName string, request T) error {
	v := reflect.ValueOf(request)

	var setClauses []string
	var args []interface{}
	for i := 0; i < v.NumField(); i++ {
		field := v.Field(i)
		jsonTag := v.Type().Field(i).Tag.Get("json")
		if jsonTag == "id" {
			args = append([]interface{}{field.Interface()}, args...) // Prepend ID to args for WHERE clause
		}

        // jsonTag = v.Type().Field(i).Tag.Get("json")
        // For PostgreSQL, use $n placeholders
        setClauses = append(setClauses, fmt.Sprintf("%s = $%d", jsonTag, len(args)+1))
        args = append(args, field.Interface())
	}

	// Assuming the ID field exists and is the first field
	if len(args) == 0 {
		return fmt.Errorf("no fields to update")
	}

	// Construct and execute the SQL statement
	sql := fmt.Sprintf("update %s set %s where id = $1", tableName, strings.Join(setClauses, ", "))
	fmt.Printf("\n\nUpdteEntity: sql: %q, args: %v", sql, args)

    _, err := Conn.Exec(context.Background(), sql, args...)
    return err
}

```
