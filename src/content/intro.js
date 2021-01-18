import style from './items.module.css';

const Intro = () =>{
    return (
        <>
        <div className={style.block}>
            <img src="photo.jpg" alt="intro"></img>
            Rahul Indhane
            <i class="fa fa-briefcase fa-fw"> Rahul Indhane</i>
            <i class="fa fa-briefcase fa-fw">Gurgaon, India</i>
            <i class="fa fa-briefcase fa-fw">email@irahul.me</i>
            <hr/>
        </div>
        <div className={style.block}>
        <h1>Skills</h1>
        <p>Python, C/C++, Java</p>
        <div className={style.progress} >60%</div>
        <hr/>
    </div>
    </>
    );
}

export default Intro;