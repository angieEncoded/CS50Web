
// Some other function
function Name(props) {
    return (
        <div>{props.name}</div>
    )
}


// All main react rendering below here
function App() {

    return (
        <div>
            <Name name="Josie" />
            "Hello"

        </div>
    )
}

ReactDOM.render(<App />, document.querySelector("#app"))






// const catbreeds =
//     [{ "breed": "Angora" }, { "breed": "Calico" }, { "breed": "Orange Tabby" }]



// var db = new Dexie("MyDatabase");
// db.version(1).stores({
//     friends: "++id, name, age, *tags",
//     breeds: "&breed"
// });


// db.open()

// db.breeds.bulkPut(catbreeds)

