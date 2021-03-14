package main

import "fmt"
import "time"

func say(s string) {
    for i := 0; i < 5; i++ {
        time.Sleep(1000 * time.Millisecond)
        fmt.Printf("idx %d %s\n", i, s)
    }
}

func main() {
    go say("hello routine1")
    say("hello")
}
