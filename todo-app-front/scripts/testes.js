// CONSUMO DE API

// TESTE 1
// function fazPost(url, body) {
//     console.log("Body=", body)
//     let request = new XMLHttpRequest()
//     request.open("POST", url, true)
//     request.setRequestHeader("Content-type", "application/json")
//     request.send(JSON.stringify(body))

//     request.onload = function() {
//         console.log(this.responseText)
//     }

//     return request.responseText
// }


// function cadastraUsuario() {
//     preventDefault()
//     let url = "http://127.0.0.1:5000/users"
//     let nome = document.getElementById("nome").value
//     let email = document.getElementById("email").value
//     console.log(nome)
//     console.log(email)

//     body = {
//         "name": nome,
//         "email": email
//     }

//     fazPost(url, body)
// }

// TESTE 2

const URL = "http://127.0.0.1:5000"

var nameUser = document.querySelector("#nameUser")
var emailUser = document.querySelector("#emailUser")
var passwordUser = document.querySelector("#passwordUser")
var passwordRepeatUser = document.querySelector("#passwordRepeatUser")
var messageAlert = document.querySelector("#messageAlert")
var resultado = document.querySelector('#resultado')

function listarUsuarios() {
    fetch(URL + "/users", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Success:", data);
        })
        .catch((error) => {
          console.error("Error:", error);
        })
}

function cadastrarUsuario() {
    if(password.value == passwordRepeat.value) {
        messageAlert.innerHTML = "Senhas estão iguais."

        const data = { 
          name: `${nameUser.value}`,
          email: `${emailUser.value}`,
          password: `${passwordUser.value}`
        }
        
        // fetch(URL + "/auth/register", {
        //   method: "POST",
        //   headers: {
        //     "Content-Type": "application/json",
        //   },
        //   body: JSON.stringify(data),
        // })
        //   .then((response) => response.json())
        //   .then((data) => {
        //     console.log("Success:", data);
        //   })
        //   .catch((error) => {
        //     console.error("Error:", error);
        //   })

          console.log(nameUser.value)
          console.log(emailUser.value)
          console.log(passwordUser.value)
          console.log(URL)


    } else {
        messageAlert.innerHTML = "Senhas não estão iguais."


    }
}


function teste() {
  const data = { 
    name: `${nameUser.value}`,
    email: `${emailUser.value}`,
    password: `${passwordUser.value}`
  }
  
  const response = fetch(URL)

  console.log(data)
  console.log(JSON.stringify(data))
  console.log(response)
}