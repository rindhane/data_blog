#!powershell
#make sure working directory or current directory is the root folder of project
#preparing resume webapp
$webapp="resume" 
rm -r static/*
rm -r $webapp/static/* ;
rm -r $webapp/templates/$webapp/* ;
cd $webapp/ ;
npm run build ; #make sure npm is installed #make sure webapp config is also updated in 
                #build script of package.json in src folder
#moving build files to django structure
mkdir -p templates/${webapp}/ ;
mv build/index.html templates/${webapp}/ ;
cp -r build/static/* static/;
rm -r build/static ;
cp -r build/* static/ 
rm -r build/*
#build transition finished
cd ../ ;
python manage.py collectstatic ; # make sure right pyenv is activated.
gcloud app deploy ; #make sure right project in Gcloud is selected 



