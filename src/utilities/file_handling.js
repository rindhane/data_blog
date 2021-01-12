const getData=(file)=>{
    return fetch(file
    ,{
      headers : { 
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Access-Control-Allow-Origin':"*",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept" 
       }
    }
    ).then(
        function(response){ 
        return response.json();}
        ).then(
        function(jsonObject){
        return JSON.stringify(jsonObject);}
        );
  }

export default getData;