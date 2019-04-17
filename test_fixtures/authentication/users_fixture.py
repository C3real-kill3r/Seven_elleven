null = None

registration_query = """
    mutation {
    registerUser(email: "brybzi@gmail.com", password: "Bry123!@#", username: "Rybczynski") {
        success
        user {
        id
        }
    }
    }
"""

registration_wrong_email_query = """
    mutation {
    registerUser(email: "brybzi.com", password: "Bry123!@#", username: "Rybczynski") {
        success
        user {
        id
        }
    }
    }
"""

registration_response = {
  "data": {
    "registerUser": {
      "success": [
        "Check your email to activate your account"
      ],
      "user": {
        "id": "1"
      }
    }
  }
}

registration_wrong_password_query = """
mutation {
    registerUser(email: "brybzi@gmai.com", password: "Pass", username: "Rybczynsk") {
        success
        user {
        id
        }
    }
    }
"""

registration_wrong_password_response = {
  "errors": [
    {
      "message": "Make sure your password is at lest 8 letters",
      "locations": [
        {
          "line": 3,
          "column": 5
        }
      ],
      "path": [
        "registerUser"
      ]
    }
  ],
  "data": {
    "registerUser": null
  }
}

login_query = """
mutation {
  logIn(email: "brybzi@gmail.com", password: "Bry123!@#") {
    user{
      username
      email
    }
    token
    }
  }
  """

login_wrong_password = """
mutation {
  logIn(email: "brybzi@gmail.com", password: "Pass12") {
    user{
      username
      email
    }
    token
    }
  }
  """

password_reset_mutation = """
  mutation{
  resetPasswrord(email:"brybzi@gmail.com")
  {
    success
    message
  }
}
"""
delete_non_existent_user_query = """
mutation {
  deleteUser(username: "Rybczynsk") {
    user {
      username
      email
    }
  }
}
"""

delete_user_query = """
mutation {
  deleteUser(username: "Rybczynski") {
    user {
      username
      email
    }
  }
}
"""
