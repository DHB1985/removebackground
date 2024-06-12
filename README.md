# Remove Background

## Installation

### Make Virtual Environment

```bash
python -m venv {name_environment}
```

Activate virtual environment in Windows

```bash
.\venv\Scripts\Activate.ps1
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## Run API

```bash
python .\src\app.py
```

## EndPoint

```bash
Type: Post
URL: http://127.0.0.1:5000/removebackground
```

### Body

```bash
{
  image: base64Image
}
```

### Responses

#### Status 200

```bash
{
  status:200,
  data: {
    imgSrc: base64Image,
    result:true
  }
}
```

#### Status 400

```bash
{
  status:400,
  data: {
    result:false
  }
}
```

### Usage (axios example)

```javascript
const data = {
  dni: string || integer,
  gender: string,
  image: base64Image
};
const headers = {
  headers: { 
    'apikey': 'apykeyvalue'
  }
}
response = axios.post('http://127.0.0.1:5000/upload', data, headers)
```

## License

[MIT](https://choosealicense.com/licenses/mit/)