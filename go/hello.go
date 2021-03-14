package main

import "fmt"

func max(num1, num2 int) int {
	var res int
	if num1 > num2 {
		res = num1
	} else {
		res = num2
	}
	return res
}

func swap(x, y string) (string, string) {
	return y, x
}

func array() {
	fmt.Print("\n\narray:\n")
	var i [10]int
	var j = [10]int{1, 2, 3}
	var k = [...]int{2, 3, 4, 5, 6}

	fmt.Println(i)
	fmt.Println(j)
	fmt.Println(k)

	j[0] = 10
	j[1] = 11
	fmt.Println(j)

}

func pointer() {
    var i int = 20
    var p *int

    p = &i
    fmt.Printf("&i = %x p = %x\n", &i, p)
    fmt.Printf("i = %d *p = %d\n", i, *p)

    p = nil
    
    if (p == nil) {
        fmt.Printf("p = nil %x\n", p)
    }
}

type book struct {
    title string
    author string
}

func struct_test() {
    fmt.Println(book{"go", "author"})
    fmt.Println(book{title: "go", author: "author"})

    var b book
    b.title = "go book"
    b.author = "zhang sanfeng"

    print_book(&b)   
}

func print_book(b *book) {
    fmt.Printf("title %s author: %s\n", b.title, b.author)
}

func slice() {
    var n = make([]int, 3, 5)

    printSlice(n)

   n1 := []int{0,1,2,3,4,5,6,7,8}   
   printSlice(n1)

   fmt.Println("numbers[1:4] =", n1[1:4])

   n1 = append(n1, 11)
   printSlice(n1)

   n2 := make([]int, len(n1), cap(n1) * 2)
   copy(n2, n1)     // n1 -> n2 
   printSlice(n1)  
   printSlice(n2)  
   
}

func printSlice(x []int) {
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)
}

func map_test() {
	fmt.Println("map:")

    var m map[string]string
    m = make(map[string]string)

	fmt.Println(m)
	// fmt.Println(m1) 

    m["a"] = "apple"
    m["b"] = "banana"

    f, ok := m[ "c" ]
    fmt.Println(f)      // 
    fmt.Println(ok)     // false
    if (ok) {
        fmt.Printf("map[c] exist\n")
    } else {
        fmt.Printf("map[c] not exist\n")
    }


}

func main() {
	fmt.Println("hello world")

	var s = 123
	var e = "456"
	var t = fmt.Sprintf("abc %d %s", s, e)
	fmt.Println(t)

	var a, b int = 1, 2
	fmt.Println(a, b)

	var ret int

	ret = max(a, b)
	fmt.Printf("max(%d, %d): %d\n", a, b, ret)

	s1, s2 := swap("google", "tasla")
	fmt.Println(s1, s2)

	array()
	pointer()
	struct_test()

	slice()
	map_test()
}
