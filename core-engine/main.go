package main
import ("fmt";"net/http")
func main() {
	fmt.Println("AI Agent Bridge - By Jeisson Alberto")
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) { http.ServeFile(w, r, "../frontend/index.html") })
	http.ListenAndServe(":18800", nil)
}
