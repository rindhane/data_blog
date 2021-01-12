import React, {useState,useEffect}  from "react";
import Project from "./content/project.js";
//import './App.css';
import getData from './utilities/file_handling.js';


const App = () => {
  const [data , setData]=useState([]);
  useEffect( () => {
    getProjects();
  },[]);
  const getProjects = async () => {
    let resp = await getData('./data/projects.json');
    resp=JSON.parse(resp);    
    setData([resp]);	
  };
  return (
      <div >
        <h1>Intro</h1>
        <h2>well</h2>
        { data.map(val=>{
	return <Project project={val} />}) }
    </div>
  );
}

export default App;
