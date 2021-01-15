import React, {useState,useEffect}  from "react";
import Project from "./content/project.js";
import getData from './utilities/file_handling.js';
import Workex from './content/workex.js';
import './App.css';
import style from './content/app.module.css';

const App = () => {
  const [data , setData]=useState([]);
  const [exps , setExps]=useState([]);
  let keys=[...Array(5).keys()];
  useEffect( () => {
    getDetails();
  },[]);
  const getDetails = async () => {
    let resp = await getData('./data/projects.json');
    resp=JSON.parse(resp);    
    setData(resp);
    resp= await getData('./data/experience.json');
    resp=JSON.parse(resp);    
    setExps(resp);	
  };
  return (
      <div >
        <div className={style.container}>
          { data.map(val => {
	            return <Project project={val} /> })}
       </div>
       <div className={style.container}>
          { exps.map(val=>{
	          return <Workex exp={val} />})}
        </div>    
    </div>
  );
}

export default App;
