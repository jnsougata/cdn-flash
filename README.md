# ☁️ cdn-flash
- A minimal cdn for deta drive files 
- Works only with files size <= 100MB
- Suitable to deliver image. Other file types should work as well


# ⚠️ warning
- Auto destroys file after 1 hour
- Requires Deta project key inside headers to cache file from drive
- No project key is being stored or used by the developer (check source)


# 🔗 endpoints
`root` https://cdn-flash.herokuapp.com

- **GET** `/url`
  - _header format_
      ``` 
      {
        'DETA-PROJECT-KEY': <YOUR-DETA-PROJECT-KEY>, 
        'DETA-DRIVE-NAME': <TARGET-DRIVE-NAME> , 
        'DETA-FILE-NAME': <TARGET-FILE-PATH>
       }
      ```
  - _JSON response_
    `{"url": "https://cdn-flash.herokuapp.com/file/{file_hash}.{file_extension}"}`

  - _sample asset url:_ https://cdn-flash.herokuapp.com/file/pcb7qy80h7eyak4rvxgp4w.png

