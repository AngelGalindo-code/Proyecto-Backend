# 400 bad request

bad_request = {
  "errors": [
    {
      "code": "Bad request",
      "message": "Solicitud incorrecta",
      "level": "error",
      "description": "Datos incorrectos"
    }
  ]
}

# 404 not found

not_found = {
  "errors": [
    {
      "code": "Not found",
      "message": "Objeto no encontrado",
      "level": "error",
      "description": "El objeto solicitado no se encuentra en la base de datos"
    }
  ]
}

# 409 conflict

conflict = {
  "errors": [
    {
      "code": "Resource conflict",
      "message": "Conflicto de recursos",
      "level": "error",
      "description": "Conflicto de recursos"
    }
  ]
}

# 500 internal server error

server_error = {
  "errors": [
    {
      "code": "Internal Server Error",
      "message": "Error de Servidor",
      "level": "error",
      "description": "Error en el lado del Servidor"
    }
  ]
}