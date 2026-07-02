package main
import ("fmt";"net/http";"os";"path/filepath")
func main() {
	ex, _ := os.Getwd()
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		p := filepath.Join(ex, "frontend", "index.html")
		if _, err := os.Stat(p); os.IsNotExist(err) { p = filepath.Join(ex, "..", "frontend", "index.html") }
		http.ServeFile(w, r, p)
	})
	fmt.Println("Dashboard: http://localhost:18800")
	http.ListenAndServe(":18800", nil)
}
