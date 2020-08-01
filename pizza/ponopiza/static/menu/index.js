document.addEventListener('DOMContentLoaded',()=>{
  document.addEventListener('click',event=>{
    const element=event.target;
    if(element.className="nav-link"){
      load(element);
    }
  });
});
function load(cat){
  const request=new XMLHttpRequest;
  request.open('POST','/result')
  request.onload = ()=>{
    const data=JSON.parse(request.responseText);
    data.forEach(add_post);
  };
  const data=new FormData();
  data.append('cat',cat);
  request.send(data);
};
const post_template=Handlebars.compile(document.querySelector('#post').innerHTML);
function add_post(content){

  const post=post_template({'contents':content});
  document.querySelector('#posts').innerHTML +=post;
};
