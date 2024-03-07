

#Initializing "data base" actually just a dict
#Later should be implemented in redis ig
users_db: dict[int, dict[str, dict[str, str]]] = {}