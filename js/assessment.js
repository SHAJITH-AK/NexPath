(() => {
  const questions=[...document.querySelectorAll(".question")];
  const counter=document.getElementById("counter"), progress=document.getElementById("progress");
  const prev=document.getElementById("prev"), next=document.getElementById("next"), submit=document.getElementById("submit");
  let current=0;
  function show(i){
    current=Math.max(0,Math.min(i,questions.length-1));
    questions.forEach((q,n)=>q.classList.toggle("active",n===current));
    counter.textContent=`Question ${current+1} of ${questions.length}`;
    progress.style.width=`${((current+1)/questions.length)*100}%`;
    prev.disabled=current===0;
    next.style.display=current===questions.length-1?"none":"inline-flex";
    submit.style.display=current===questions.length-1?"inline-flex":"none";
  }
  function answered(i){ return !!questions[i].querySelector("input:checked"); }
  next.addEventListener("click",()=>{ if(!answered(current)){alert("Please select an answer before continuing.");return;} show(current+1); });
  prev.addEventListener("click",()=>show(current-1));
  document.getElementById("testForm").addEventListener("submit",e=>{
    if(questions.some((q)=>!q.querySelector("input:checked"))){e.preventDefault();alert("Please answer all 10 questions.");}
  });
  show(0);
})();