# ☁️ cdn-flash
- A minimal cdn for deta drive files. 
- Works only with files size less than 50mb
- Suitable to deliver image. Other file types should work as well


# ⚠️ warning
- Requires Deta project key inside headers to cache file from drive
- No project key is being stored or used by the developer
- Auto destroys file after 5 minutes

# 🔗 endpoints
`root` https://cdn-flash.herokuapp.com

- **POST** `/cdn`
  - _header format_
      ``` 
      {
          'DETA-PROJECT-KEY': <YOUR-DETA-PROJECT-KEY>, 
          'DRIVE-NAME': <TARGET-DRIVE-NAME> , 
          'FILE-NAME': <TARGET-FILE-PATH>
       }
      ```
  - _JSON response_
    `{"url": "https://cdn-flash.herokuapp.com/file/{project_id}_{file_name}"}`
