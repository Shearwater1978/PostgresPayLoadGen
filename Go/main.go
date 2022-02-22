package main

import (
    "log"
    "net/http"
    "encoding/json"
    "github.com/julienschmidt/httprouter"
    "fmt"
    "strconv"
    "database/sql"
    "gopkg.in/ini.v1"
    "os"
    _ "github.com/lib/pq"
)

type server struct{}

type People struct {
  FIO      string `json:"fio"`
  Phone    string `json:"phone"`
  Age         int `json:"age"`
  City     string `json:"city"`
  Address  string `json:"address"`
  Inn      string `json:"inn"`
}

/*
type oneman struct{
  fio string
  phone string
  age int
  city string
  address string
  inn int
}
*/

func read_ini() (string){
    var connString,dbuser,dbname,dbpass,dbport,dbhost string
    cfg, err := ini.Load("/opt/posgtresql.ini")
    if err != nil {
        fmt.Printf("Fail to read file: %v", err)
        os.Exit(1)
    }
    dbuser = cfg.Section("postgresdb").Key("db_user").String()
    dbname = cfg.Section("postgresdb").Key("db_name").String()
    dbpass = cfg.Section("postgresdb").Key("db_pass").String()
    dbport = cfg.Section("postgresdb").Key("db_port").String()
    dbhost = cfg.Section("postgresdb").Key("db_host").String()
    connString = "user="+dbuser+" password="+dbpass+" dbname="+dbname+" port="+dbport+" host="+dbhost+" sslmode=disable"
    return connString
  }

func addRecord(w http.ResponseWriter, r *http.Request,
               _ httprouter.Params) {

  var rec People

  err := json.NewDecoder(r.Body).Decode(&rec)
  if err != nil || rec.FIO == "" || rec.Phone == "" || strconv.Itoa(rec.Age) == "" || rec.City == "" || rec.Address == "" || rec.Inn == ""{
    w.WriteHeader(400)
    fmt.Println(err)
    return
  }
  connStr := read_ini()
  db, err := sql.Open("postgres", connStr)

  if err != nil {
    log.Fatal(err)
    }
  insertDb(db, rec.FIO, rec.Phone, rec.Age, rec.City, rec.Address, rec.Inn)
  w.WriteHeader(201)
  defer db.Close()
}

func insertDb(db *sql.DB, fio string, phone string,age int,city string, address string,inn string){

  result, err := db.Exec("INSERT INTO people VALUES ('"+fio+"','"+phone+"','"+strconv.Itoa(age)+"','"+city+"','"+address+"','"+inn+"')")

  if err != nil{
     panic(err)
     }
  fmt.Println(result.RowsAffected())
}


func main() {
  r := httprouter.New()
  r.POST("/api/v1/records", addRecord)
  log.Fatal(http.ListenAndServe(":18080", r))
 }
