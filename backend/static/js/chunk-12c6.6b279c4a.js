(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-12c6"],{88:function(n,t){},zd34:function(n,t,e){"use strict";e.r(t),e.d(t,"export_txt_to_zip",function(){return c});var i=e("fDnD"),o=e.n(i);function c(n,t,e,i){var c=new o.a,r=e||"file",f=i||"file",u=n+"\r\n";t.forEach(function(n){var t;t=n.toString(),u+=t+"\r\n"}),c.file(r+".txt",u),c.generateAsync({type:"blob"}).then(function(n){saveAs(n,f+".zip")},function(n){alert("导出失败")})}e("MnM9")}}]);