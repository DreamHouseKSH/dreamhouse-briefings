// Run on an opened daily page: playwright-cli run-code --filename scripts/check-daily-browser.js
// Browser geometry regression check; no model, network write or audio synthesis.
async (page) => {
  const results=[];
  for(const [width,height] of [[390,844],[844,390]]) {
    await page.setViewportSize({width,height});
    if(await page.locator('.day-focused').count())await page.getByRole('button',{name:'닫기 ✕',exact:true}).click();
    await page.getByRole('button',{name:'집중 보기',exact:true}).click();
    const boxes=await page.evaluate(()=>{
      const box=selector=>{const r=document.querySelector(selector).getBoundingClientRect();return {top:r.top,bottom:r.bottom,height:r.height}};
      return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:innerHeight,controls:box('.day-controls'),stage:box('.day-stage'),chapters:box('.day-chapters'),close:box('[data-action=close-focus]')};
    });
    if(boxes.scrollWidth!==boxes.width || boxes.stage.top<boxes.controls.bottom-1 || boxes.stage.bottom>boxes.chapters.top+1 || boxes.close.bottom>boxes.height || boxes.stage.height<50)throw Error('Focus controls overlap content: '+JSON.stringify(boxes));
    results.push(boxes);
    await page.getByRole('button',{name:'닫기 ✕',exact:true}).click();
  }
  return results;
}
