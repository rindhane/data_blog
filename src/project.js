import React from "react";

let project = '[{"name" : "first", "age" : "20"},\
            {"name" : "while", "age" : "20"}]' ;
var mydata = JSON.parse(project);
console.log(mydata[0].name);

function Project(props) {
    return (
        <div>
            <h2>New Title</h2>
            <ul>
            <li>Carried out the analysis to estimate the call premiums using the Black-Scholes-Merton equation.</li>
            <li>Built function to scrape the live data of the derivatives from BSE site drive the analysis in real time to extend it to algorithmic trading</li>
            <li>Created API methods to produce local database in sqlite of historical records of stock prices from the BSE website.</li>
            </ul>   
        </div>
    );
}

export default Project;
