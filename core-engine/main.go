package main
import (
	"fmt"
	"log"
	"net/http"
)
func main() {
	fmt.Println("AI Agent Core Engine - Desarrollado por Jeisson Alberto")
	http.HandleFunc("/webhook", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "AI Agent: Message Orchestrated by Jeisson Alberto Bridge")
	})
	log.Fatal(http.ListenAndServe(":18800", nil))
}
