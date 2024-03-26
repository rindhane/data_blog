import React, {useState,useEffect}  from "react";
import Project from "./content/project.js";
import getData from './utilities/file_handling.js';
import Workex from './content/workex.js';
import Education from './content/education.js';
import style from './content/app.module.css';
import Intro from "./content/intro.js";
import static_url from './static_url.js';

const AboutApp = () => {
  const [data , setData]=useState([]);
  const [exps , setExps]=useState([]);
  const [certi , setCerti]=useState([]);
  useEffect( () => {
    getDetails();
  },[]);
  const getDetails = async () => {
    let resp = await getData(static_url('projects'));
    resp=JSON.parse(resp);    
    setData(resp);
    resp= await getData(static_url('workex'));
    resp=JSON.parse(resp);    
    setExps(resp);
    resp= await getData(static_url('certificates'));
    resp=JSON.parse(resp);    
    setCerti(resp);	
  };
  return (
      <grid className={style.color}>
        <section>
          <div className={style.container}>
            <Intro certi={certi} />
          </div>
        </section>
        <section>
          <div className={style.container}>
            <div className={style.heading}>
                  <a href='https://in.linkedin.com/in/rindhane'>
                    <i className="fa fa-linkedin-square" aria-hidden="true"></i>
                  </a>
                  <span className={style.title}>Work Experience</span> 
            </div> 
            { exps.map((val,index)=>{
              return <Workex key= {index} exp={val} />})}
          </div>
          <div className={style.container}>
            <div className={style.heading}>
                    <i className="fa fa-tasks " aria-hidden="true"></i>
                    <span className={style.title}>Data Science Projects</span> 
            </div> 
            { data.map((val,index) => {
                  return <Project key={index} project={val} /> })}
          </div>
          <div className={style.container}>
            <div className={style.heading}>
            <i className="fa fa-book" aria-hidden="true"></i>
              <span className={style.title}>Education</span> 
            </div> 
            <Education />
          </div> 
        </section>  
      </grid>
  );
}

export default AboutApp;
