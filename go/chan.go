package main

import "fmt"

func sum(i []int, c chan int) {
	s := 0
	for _, v := range i {
		s += v
	}
	c <- s
}

func main() {
	s := []int{1, 2, 3, 4, 5}
	c := make(chan int)
	
	go sum(s[:len(s)/2], c)
	go sum(s[len(s)/2:], c)
	x, y := <-c, <-c

	fmt.Println(x, y, x+y)

}
