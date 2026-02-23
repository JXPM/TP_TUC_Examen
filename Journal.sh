# Créer un nouveau dépôt GitHub 
git init
git branch -M main
git add .
git commit -m "first commit"
gh repo create bar-saas-backend --private
git remote add origin https://github.com/JXPM/TP_TUC_Exam.git
git push --set-upstream origin main