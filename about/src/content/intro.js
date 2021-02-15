import style from './items.module.css';


const Intro = (props) =>{
    let certi=props.certi;
    return (
        <div className={style.section}>
                <img src="/static/about/data/photo.jpg" alt="img"></img>
                <h3 style={{textAlign:'center'}}>Rahul Indhane</h3>
                <div className={style.category}>
                    <i className="fa fa-user-circle-o" aria-hidden="true"> Rahul Indhane
                    </i><br/>
                    <i className="fa fa-briefcase "> Project Manager, Solution Architect</i><br/>
                    <i className="fa fa-home"> Pune, India</i><br/>
                    <i className="fa fa-envelope"> email@irahul.me</i><br/>
                    <i className="fa fa-phone"> +91-8130848031</i><br/>
                    <i className="fa fa-wpforms" aria-hidden="true"><a href="https://drive.google.com/file/d/1Oo-2DhAy8sx-PJYsF2CUA7cmHfoeNafO/view?usp=sharing"> Resume</a></i>
                    
                </div>
            <hr/>
            <div>
                <i className="fa fa-superpowers fa-2x" aria-hidden="true"></i>
                <span className={style.sectionHeading}>Skills</span> 
            </div> 
            <div className={style.category}>   
                <p>Python, C/C++, Java</p> 
                <div className={style.progress} style={{width: "80%"}}>80%</div>
                <p>HTML, CSS, JavaScript, SQL</p>
                <div className={style.progress} style={{width: "75%"}}>75%</div>
                <p>Statistical Modelling</p>
                <div className={style.progress} style={{width: "75%"}}>75%</div>
                <p>Tensorflow, Pytorch, Scikit</p>
                <div className={style.progress} style={{width: "60%"}}>60%</div>
                <p>Git, Linux Administration</p>
                <div className={style.progress} style={{width: "75%"}}>75%</div>
                <p>GCloud, AWS</p>
                <div className={style.progress} style={{width: "50%"}}>50%</div>
            </div>
            <hr/>
            <div>
                <i className="fa fa-id-card fa-2x" aria-hidden="true"></i>
                <span className={style.sectionHeading}>Certifications</span> 
            </div>
            <div className={style.category}>
                {certi.map((cert,index)=>{
                    return (
                    <div key={index}>
                        <i className="fa fa-star" aria-hidden="true"></i>
                        <a href={cert.link}>{cert.title}</a>
                        <div className={style.sideRight}>
                            <i className="fa fa-university" aria-hidden="true"></i>
                            {cert.provider}
                        </div>
                        <div>{cert.content}</div>
                        <br/> 
                    </div>);
                })}
            </div>            
        </div>
    );
}

export default Intro;