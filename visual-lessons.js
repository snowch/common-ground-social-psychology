// Original visual explanations. Numeric examples are explicitly illustrative.
function figureIcon(kind,x,y){
 if(['person','sam','maya'].includes(kind))return person(x,y-9,kind==='sam'?'#A1486D':kind==='maya'?'#806196':'#236A67',.32);
 if(kind==='clock')return `<circle cx="${x}" cy="${y}" r="21" fill="#F2F6FC" stroke="#216B88" stroke-width="2"/><path d="M${x} ${y-13}V${y}L${x+11} ${y+6}" fill="none" stroke="#216B88" stroke-width="2"/>`;
 if(kind==='door')return `<path d="M${x-19} ${y+23}V${y-23}H${x+19}V${y+23}M${x+8} ${y}H${x+11}" fill="#F2F6FC" stroke="#216B88" stroke-width="2"/>`;
 return `<rect x="${x-20}" y="${y-24}" width="40" height="48" rx="4" fill="#F2F6FC" stroke="#216B88" stroke-width="2"/><path d="M${x-12} ${y-12}H${x+12}M${x-12} ${y}H${x+12}M${x-12} ${y+12}H${x+7}" stroke="#216B88" stroke-width="2"/>`;
}
function figureFooter(lines){return (Array.isArray(lines)?lines:[lines]).map((line,i,a)=>label(260,a.length===1?444:423+i*28,line,19)).join('');}
function compareFigure(key,title,left,right,footer){
 const column=(x,item,color)=>{const heads=Array.isArray(item[0])?item[0]:[item[0]];return heads.map((t,i)=>label(x+110,heads.length===1?88:72+i*25,t,21,color)).join('')+`<rect x="${x}" y="121" width="220" height="265" rx="14" fill="#FFF" stroke="${color}" stroke-width="1.5"/>`+figureIcon(item[2]||'record',x+110,164)+item[1].map((t,i)=>label(x+110,219+i*29,t,20)).join('');};
 return conceptSVG(key,[title,...[left[0]].flat(),...left[1],...[right[0]].flat(),...right[1],...(Array.isArray(footer)?footer:[footer])].join('. '),label(260,29,title,23)+column(20,left,'#7058A3')+column(280,right,'#216B88')+figureFooter(footer));
}
function flowFigure(key,title,steps,footer){
 const body=steps.map((lines,i)=>{const y=61+i*89;return `<rect x="75" y="${y}" width="370" height="65" rx="12" fill="#FFF" stroke="${i===0?'#7058A3':'#8DA6B7'}" stroke-width="1.5"/>`+lines.map((t,j)=>label(260,y+(lines.length===1?40:27+j*25),t,j===0?21:19)).join('')+(i<steps.length-1?conceptArrow(260,y+69,260,y+84):'');}).join('');
 return conceptSVG(key,[title,...steps.flat(),footer].join('. '),label(260,27,title,23)+body+figureFooter(footer));
}
function threeRowsFigure(key,title,rows,footer){return conceptSVG(key,[title,...rows.flat(),footer].join('. '),label(260,28,title,23)+rows.map((r,i)=>{const y=65+i*108;return `<rect x="25" y="${y}" width="470" height="89" rx="13" fill="#FFF" stroke="#8DA6B7" stroke-width="1.5"/>`+label(260,y+30,r[0],23,i===0?'#7058A3':'#216B88')+label(260,y+64,r[1],20);}).join('')+figureFooter(footer));}
function personSituationFigure(){return conceptSVG('person-situation','A hypothetical example: a disposition of usual patience and a situation with several visitors may both contribute to one sharp reply. Compare calmer and busier shifts before inferring a lasting tendency.',
 `<text x="260" y="30" text-anchor="middle" font-family="CourseSerif,Georgia,serif" font-size="24" fill="#19394D">A tendency meets a busy room</text>
 <rect x="24" y="58" width="222" height="180" rx="12" fill="#F8F5FC" stroke="#C5D3E5"/>
 <rect x="274" y="58" width="222" height="180" rx="12" fill="#FFFFFF" stroke="#C5D3E5"/>`+
 label(135,89,'Disposition',21,'#7058A3')+label(385,89,'Situation',21,'#216B88')+
 figureIcon('person',135,129)+figureIcon('person',353,129)+figureIcon('person',385,129)+figureIcon('person',417,129)+
 label(135,188,'Usually patient',21)+label(135,215,'with visitors',18,'#4B6172')+
 label(385,188,'Several visitors',21)+label(385,215,'need help at once',18,'#4B6172')+
 conceptArrow(135,246,212,300,true,'#8DA6B7')+conceptArrow(385,246,308,300,true,'#8DA6B7')+label(260,276,'may contribute',15,'#4B6172')+
 `<rect x="94" y="310" width="332" height="80" rx="12" fill="#FFFFFF" stroke="#216B88" stroke-width="1.5"/>`+
 label(260,339,'Observed action',17,'#4B6172')+label(260,372,'One sharp reply',25)+label(260,441,'Compare calmer and busier shifts.',19,'#216B88'));}
function observationFigure(){return conceptSVG('observation-attribution','Leo’s observation is that Maya arrived after the start. His attribution that she does not care proposes a cause. The cause needs evidence.',
 `<text x="260" y="30" text-anchor="middle" font-family="CourseSerif,Georgia,serif" font-size="24" fill="#19394D">Two different questions</text>
 <rect x="24" y="68" width="222" height="242" rx="12" fill="#FFFFFF" stroke="#C5D3E5"/>
 <rect x="274" y="68" width="222" height="242" rx="12" fill="#FFFFFF" stroke="#C5D3E5"/>`+
 label(135,104,'Observation',22,'#216B88')+label(385,104,'Attribution',22,'#7058A3')+
 figureIcon('clock',135,151)+`<circle cx="385" cy="151" r="21" fill="#F8F5FC" stroke="#7058A3" stroke-width="2"/>`+label(385,162,'?',30,'#7058A3')+
 label(135,210,'Maya arrived',22)+label(135,239,'after the start.',21)+label(385,224,'“She doesn’t care.”',21)+
 label(135,281,'A recorded action',17,'#4B6172')+label(385,281,'A proposed cause',17,'#4B6172')+
 label(260,365,'One statement records an action.',21)+label(260,397,'The other proposes a cause.',21)+label(260,444,'What evidence could test Leo’s cause?',18,'#216B88'));}
function actorObserverFigure(){return compareFigure('actor-observer','One observer, two explanations',
 ['Leo explains himself',['“The bus','was delayed.”','Circumstances'],'person'],
 ['Leo explains Maya',['“She doesn’t care.”','A personal tendency','Could he be missing','her circumstances?'],'person'],
 ['A possible actor–observer difference.','The pattern depends on judgment and setting.']);}
function repeatedEvidenceFigure(){
 const steps=[
  ['Describe the action','Maya arrived after the start.','Keep the cause open.'],
  ['Compare occasions','Is lateness usual across shifts?','Look for exceptions.'],
  ['Check alternatives','Could a travel barrier explain it?','Ask Maya about the delay.'],
  ['Revise your confidence','Weigh the evidence for each cause.','Allow your explanation to change.']];
 const leftText=(x,y,t,size,color='#19394D',extra='')=>`<text x="${x}" y="${y}" text-anchor="start" font-family="CourseSans,Arial,sans-serif" font-size="${size}" fill="${color}" ${extra}>${esc(t)}</text>`;
 return `<svg viewBox="0 0 520 580" role="img" data-diagram="repeated-evidence" aria-label="Test an attribution: describe Maya’s late arrival, compare occasions, check alternatives, and revise confidence from evidence.">
 <text x="30" y="35" font-family="CourseSerif,Georgia,serif" font-size="26" fill="#19394D">Follow the evidence</text>
 <rect x="30" y="58" width="460" height="68" rx="12" fill="#F9FBFD"/>
 ${leftText(48,82,'Leo’s proposed cause',14,'#4B6172')}${leftText(48,110,'“She doesn’t care.”',23,'#7058A3')}
 <path d="M51 167V458" fill="none" stroke="#ADC6D3" stroke-width="2"/>
 ${steps.map((row,i)=>{const y=171+i*95;return `<circle cx="51" cy="${y}" r="18" fill="${i===3?'#216B88':'#FFFFFF'}" stroke="#216B88" stroke-width="1.5"/><text x="51" y="${y+6}" text-anchor="middle" font-family="CourseSans,Arial,sans-serif" font-size="17" fill="${i===3?'#FFFFFF':'#216B88'}">${i+1}</text>`+leftText(87,y-5,row[0],22,'#19394D','font-weight="600"')+leftText(87,y+24,row[1],18)+leftText(87,y+48,row[2],17,'#4B6172');}).join('')}
 <text x="260" y="554" text-anchor="middle" font-family="CourseSans,Arial,sans-serif" font-size="17" fill="#216B88">Let evidence change your confidence.</text></svg>`;
}
function samplingFigure(){return flowFigure('sampling-assignment','A possible selection-and-allocation design',[
 ['Population','Residents we want to learn about'],['Random sampling','Select people by chance'],['Sample enters the comparison','Who was actually included?'],['Random assignment','Allocate invitation A or B by chance']], 'Assignment does not make a sample representative.');}
function correlationFigure(){return compareFigure('correlation-causation','Together does not establish because',
 ['Observed pattern',['Poster changed.','Attendance rose.','Two things varied','together.'],'record'],
 ['Possible explanations',['Poster?','Weather?','Publicity?','What would separate','these explanations?'],'record'],
 ['Correlation describes a relationship.','A causal claim needs a fairer test.']);}
function differenceFigure(){
 const bar=(y,n,name,color)=>label(260,y-14,name,22)+`<rect x="70" y="${y}" width="380" height="42" rx="6" fill="#FFF" stroke="#8DA6B7"/><rect x="70" y="${y}" width="${380*n/100}" height="42" fill="${color}"/>`+label(260,y+77,`${n} of 100 households attend`,21);
 return conceptSVG('effect-size','Invented example: attendance is 12 of 100 versus 15 of 100 households. The observed difference is three percentage points; the estimate remains uncertain.',label(260,28,'Invented attendance example',24)+bar(100,12,'Invitation A','#7058A3')+bar(246,15,'Invitation B','#216B88')+label(260,391,'15% − 12% = 3 percentage points',25)+figureFooter('A different sample could give a different estimate.'));
}
function significanceFigure(){return compareFigure('significance-importance','Two questions about a result',
 [['Statistical','significance'],['How unusual under','a specified model?','Often a model of','no group difference.'],'record'],
 [['Practical','importance'],['How large is','the difference?','Is it useful enough','for the decision?'],'record'],
 ['Significance does not measure usefulness.','Nonsignificance does not prove zero effect.']);}
function researchCycleFigure(){return flowFigure('research-reliability','Build confidence through checks',[
 ['Preregister','Record the plan before results'],['Run a sound comparison','Sample size can improve precision'],['Share methods and materials','Make the work inspectable'],['Replicate independently','Check how dependable the finding is']], 'A larger sample cannot fix a biased comparison.');}
function availabilityFigure(){
 const cells=Array.from({length:40},(_,i)=>{const x=60+(i%10)*40,y=196+Math.floor(i/10)*38;return `<rect x="${x}" y="${y}" width="27" height="27" rx="4" fill="${i<4?'#F3E7EE':'#FFF'}" stroke="${i<4?'#A1486D':'#8DA6B7'}"/>`+(i<4?`<path d="M${x+7} ${y+7}L${x+20} ${y+20}M${x+20} ${y+7}L${x+7} ${y+20}" stroke="#A1486D" stroke-width="2"/>`:`<path d="M${x+6} ${y+14}L${x+11} ${y+19}L${x+21} ${y+7}" fill="none" stroke="#216B88" stroke-width="1.7"/>`);}).join('');
 return conceptSVG('availability-base-rate','A vivid failed repair is easy to remember. In the invented record, four failures among forty comparable repairs give a ten percent failure rate. Count the whole denominator, with consistent follow-up.',label(260,27,'A vivid case needs a denominator',23)+thoughtPanel(95,58,330,82,['“That toaster failed again!”'])+label(260,172,'Invented record: all comparable repairs',20)+cells+label(260,391,'4 failures / 40 repairs = 10%',25)+figureFooter('Availability is a shortcut, not a frequency count.'));
}
function motivatedReasoningFigure(){return flowFigure('motivated-reasoning','A desired conclusion can shape reasoning',[
 ['Maya wants the café to succeed','“I hope our repairs are working.”'],['Reassuring stories feel persuasive','Returns get less attention'],['Maya can use one test for all cases','Define failure and follow up consistently'],['Maya can invite a challenging review','What could change her first belief?']], 'A wanted conclusion can still be correct.');}
function biasCheckFigure(){return compareFigure('bias-evidence','Checking someone else’s estimate',
 ['Possible distortion',['Vivid cases get','too much attention.','The record does','not support the','initial estimate.'],'record'],
 ['Possible expertise',['Remembered cases','reflect experience.','A representative','record supports','the estimate.'],'record'],
 ['Compare their estimate with a relevant record.','Ask which cases they considered.']);}
function dissonanceFigure(){return conceptSVG('cognitive-dissonance','Maya sees a conflict between choosing reliable tools and a booking system that loses reservations. The conflict can motivate discomfort reduction through changing behavior, revising a belief, or adding a justification.',
 label(260,27,'When beliefs and actions clash',24)+box(20,65,230,88,'“I choose reliable tools.”','#FFF')+box(270,65,230,88,'“This tool loses bookings.”','#FFF')+
 conceptArrow(135,168,230,221)+conceptArrow(385,168,290,221)+box(140,239,240,58,'Possible discomfort','#ECE6F5')+
 conceptArrow(210,307,100,349)+conceptArrow(260,307,260,349)+conceptArrow(310,307,420,349)+
 box(15,365,150,52,'Change action','#FFF')+box(185,365,150,52,'Revise belief','#FFF')+box(355,365,150,52,'Add a reason','#FFF')+figureFooter('Cognitions are beliefs and knowledge about actions.'));
}
function dissonanceEvidenceFigure(){return compareFigure('dissonance-evidence','A tested prediction and a broader theory',
 [['Specific','procedure'],['Argue for a position','you do not hold.','More or less choice.','Primary difference','was not supported.'],'record'],
 [['Broader','framework'],['Inconsistency can','motivate change','or justification.','Other predictions','need their own tests.'],'record'],
 ['The 2024 replication tests a particular procedure.','Its result does not settle every dissonance claim.']);}
function authorityFigure(){return compareFigure('compliance-obedience','A request and an authority’s order',
 ['Compliance',['Leo asks Sam:','“Cover my shift?”','Sam agrees to','the request.'],'person'],
 ['Obedience',['The chair instructs:','“Skip the check.”','The authority role','can add pressure.'],'person'],
 ['An authority’s request can involve both.','People can question or resist.']);}
function safetyVoiceFigure(){return flowFigure('questioning-authority','Make questioning practically possible',[
 ['A required check is bypassed','Notice the concern'],['Pause the unsafe work','Use an agreed stop rule'],['Raise the concern','Use the agreed escalation route'],['Review before proceeding','Relevant training and responsibilities']], 'An instruction does not remove accountability.');}
function classicStudiesFigure(){return compareFigure('study-context','Different tasks, specific pressures',
 ['Asch’s task',['Compare line','lengths after','a majority gives','incorrect answers.','Some people resist.'],'record'],
 ['Milgram’s task',['An experimenter','urges continuation.','Participants believe','another person','receives shocks.'],'record'],
 ['Methods, ethics, and conditions matter.','These are not universal obedience rates.']);}
function processingFigure(){return conceptSVG('message-processing','The same person can examine a message more or less carefully according to motivation and ability. Peripheral cues and relevant arguments can play different roles across decisions.',
 label(260,27,'How carefully is the message examined?',23)+`<path d="M60 108H460" stroke="#8DA6B7" stroke-width="4"/><path d="M60 102L48 108L60 114M460 102L472 108L460 114" fill="none" stroke="#8DA6B7" stroke-width="2"/>`+label(115,77,'Less examination',19)+label(404,77,'More examination',19)+label(260,152,'Motivation + ability',22)+
 box(20,195,220,61,'Peripheral processing','#FFF')+box(280,195,220,61,'Central processing','#FFF')+label(130,296,'Familiar face',21)+label(130,329,'Credible source',21)+label(390,296,'Shift length',21)+label(390,329,'Relevant support',21)+
 figureFooter(['The elaboration likelihood model','describes processing, not fixed types of person.']));}
function attitudeFigure(){return compareFigure('attitude-evaluation','An attitude is an evaluation',
 ['Possible evaluation',['“Volunteering is','worthwhile.”','Reasons and values','shape the judgment.'],'person'],
 ['A different question',['Will I sign up?','Time, transport,','support, and choice','also affect action.'],'clock'],
 ['A positive attitude does not guarantee action.','Ask what outcome the message needs to support.']);}
function normsFigure(){return compareFigure('social-norms','What happens and what is approved',
 ['Descriptive norm',['“Many residents','volunteer.”','A claim about','what people do.'],'record'],
 ['Injunctive norm',['“Our community','values volunteering.”','A claim about','what people approve.'],'person'],
 ['These are example claims; check their truth.','Highlighting low participation can normalize it.']);}
function honestRequestFigure(){return flowFigure('honest-request','Help someone make an informed choice',[
 ['A relevant reason','What would this contribution achieve?'],['A concrete commitment','Time, effort, and available support'],['An easy next step','Ask questions or try a supported shift'],['Room to decline','Measure understanding and informed choice']], 'Remove unsupported claims about what others do.');}
function persuasionOutcomesFigure(){return flowFigure('persuasion-outcomes','Measure the outcome that matters',[
 ['Attention','An invitation gets a click'],['Understanding','The person knows the commitment'],['Informed sign-up','Participation is freely chosen'],['Continued participation','Check experience and retention']], 'A click alone does not establish these later outcomes.');}
function identityFigure(){return compareFigure('ingroup-favoritism','Who counts as “our team”?',
 ['Repair volunteers',['“Give our team','first choice of shifts.”','Group membership','can shape preference.'],'person'],
 ['Welcome volunteers',['Their contribution','can be overlooked.','Favoritism can','create unequal access','without explicit hatred.'],'person'],
 ['Check workload, incentives, and decision power.','A shared name alone does not change those.']);}
function sharedGoalFigure(){return flowFigure('shared-goal','One visitor experience needs both teams',[
 ['Welcome the visitor','Understand the need'],['Plan the repair','Agree roles and resources'],['Coordinate the handover','Tools, timing, and information'],['Review the visitor experience','Share credit, burdens, and decisions']], 'A shared goal needs workable arrangements.');}
function loafingCoordinationFigure(){return compareFigure('loafing-coordination','Similar poor output, different processes',
 ['Social loafing',['Individual effort','falls in pooled work.','“My contribution','will go unnoticed.”','A possible process.'],'person'],
 ['Coordination loss',['Effort can be high.','Work is duplicated.','A needed tool','arrives too late.','Tasks do not align.'],'clock'],
 ['An unfinished task alone does not identify either.','Check effort, tools, sequencing, and roles.']);}
function groupthinkFigure(){return flowFigure('groupthink','Agreement can hide unspoken doubts',[
 ['Pressure for agreement','Relevant concerns remain unspoken'],['Examine the actual process','Whose information was missed?'],['Collect independent views','Make contrary evidence discussable'],['Review the decision','Clear roles and structured disagreement']], 'A poor decision alone does not establish groupthink.');}
function prejudiceFigure(){return threeRowsFigure('belief-attitude-action','Three related, distinct concepts',[
 ['Stereotype: a group belief','“Every newcomer lacks repair skills.”'],['Prejudice: an attitude','“I dislike newcomers before meeting them.”'],['Discrimination: unequal treatment','Reject someone for being a newcomer.']], 'These need not form an inevitable sequence.');}
function structuralBarrierFigure(){return flowFigure('structural-barriers','A welcoming intention can leave barriers',[
 ['Recruit through existing friends','Who never hears about the opportunity?'],['Require personally owned tools','Who lacks the resources to enter?'],['Meet during working hours','Who cannot attend?'],['Inspect the process and outcomes','Intentions alone cannot establish fairness']], 'Rules can favor an existing group.');}
function contactFigure(){return compareFigure('intergroup-contact','Sharing a room and sharing participation',
 ['Limited participation',['Newcomers watch.','Established members','control the tools','and decisions.'],'door'],
 ['Cooperative contact',['Work on a shared','goal.','Share relevant tools','and decision-making.','Organizers support','equal participation.'],'person'],
 ['Intergroup contact can help under some conditions.','Check actual access and participation.']);}
function proceduralChangeFigure(){return compareFigure('procedural-change','Change the barrier in the process',
 ['Existing rule',['Apply through','existing friends.','Bring your own','specialist tools.'],'door'],
 ['A proposed change',['Open the application.','Use relevant criteria.','Provide shared tools','where feasible.','Track participation.'],'door'],
 ['A friendly encounter alone leaves the rule intact.','Use follow-up and protect privacy.']);}
function prejudiceMeasuresFigure(){return threeRowsFigure('attitude-measures','Different measures answer different questions',[
 ['Explicit attitude','What someone reports directly'],['Implicit association','An indirect response pattern in a task'],['Behavior and access','Who can apply, progress, and participate?']], 'No single score is a complete character diagnosis.');}
function opportunityFigure(){return flowFigure('relationship-opportunity','A shared shift creates opportunities',[
 ['Sam and Leo meet on Thursdays','Proximity changes who becomes familiar'],['They discover an interest in radios','Similarity can support conversation'],['They choose further conversation','Look for reciprocal interest'],['Either person can set a boundary','Contact creates no right to friendship']], 'Connection is possible, not guaranteed.');}
function exposureFigure(){return compareFigure('mere-exposure','Repeated encounters can have different effects',
 ['Possible familiarity',['A face becomes','more comfortable','to see.','Liking may increase.'],'person'],
 ['A different response',['Unwanted contact','can intensify','annoyance or threat.','More is not','automatically better.'],'person'],
 ['The mere exposure effect depends on conditions.','A stated boundary still matters.']);}
function responsivenessFigure(){return flowFigure('disclosure-responsiveness','Closeness depends on the response',[
 ['Leo discloses something personal','“It has been a difficult week.”'],['Sam listens and checks understanding','“Have I understood what you mean?”'],['Sam asks what support Leo wants','Listening, practical help, or advice?'],['Reciprocity over time','Mutual consideration, not matching secrets']], 'Disclosure needs willingness and responsiveness.');}
function attachmentBoundaryFigure(){return compareFigure('attachment-boundary','A declined invitation is useful information',
 ['What Sam says',['“I need time alone.”','An expressed','preference for now.'],'sam'],
 ['Leo’s response',['Accept the refusal.','Leave future contact','optional.','One occasion does not','establish an','attachment style.'],'person'],
 ['Attachment labels describe studied patterns.','They are not diagnoses or permission to persist.']);}
function relationshipEvidenceFigure(){return compareFigure('relationship-evidence','An association and an individual relationship',
 ['Study reports',['Some partners report','greater similarity','and satisfaction.','Self-reports can','have limitations.'],'record'],
 ['Sam and Leo’s situation',['Ask Sam and Leo','about their experiences','and preferences.','A group average','cannot choose','their goals.'],'person'],
 ['Association alone does not establish an intervention.','Ask about the pair’s actual experience.']);}
function helpingPathFigure(){return flowFigure('helping-path','Turn concern into a safe path to action',[
 ['Notice and interpret the need','Clarify what is happening'],['Accept responsibility','Agree who will take the next step'],['Identify an appropriate safe action','Use available skills, training, and support'],['Act and review','For a low-risk task, check the outcome']], 'In emergencies, follow local guidance and training.');}
function aggressionFigure(){return conceptSVG('anger-aggression','Anger is a feeling. Aggression is behavior intended to harm. Frustration, learned expectations, and perceived threat can contribute without making harm inevitable. A constructive response remains possible.',
 label(260,27,'Anger does not dictate the next action',23)+box(140,68,240,62,'Anger: a feeling','#ECE6F5')+label(260,169,'The next response can differ',22)+conceptArrow(230,188,130,245)+conceptArrow(290,188,390,245)+
 box(20,262,220,71,'Act to cause harm','#FFF')+box(280,262,220,71,'Constructive response','#FFF')+label(130,371,'Aggression',23)+label(390,371,'Reduce tension',22)+figureFooter(['De-escalation aims to reduce the risk of harm.','Context helps explain behavior; accountability remains.']));}
function cooperationFigure(){return flowFigure('cooperation-plan','Make a shared task workable',[
 ['A clear shared outcome','What needs to be done?'],['Named roles and resources','Who owns each step and has support?'],['A route for reporting problems','What happens if the plan becomes unsafe?'],['Feedback and a fair division','Review contributions, benefits, and burdens']], 'For example, name who checks the replacement shelf.');}
function proxyMeasuresFigure(){return compareFigure('proxy-and-context','A research measure and a real-world decision',
 ['Controlled measure',['An unpleasant-noise','task measures one','laboratory response.','It is an imperfect','proxy for serious','violence.'],'record'],
 ['Real-world context',['Danger, relationships,','training, and support','can change what','safe help is possible.','Crowds can also help.'],'person'],
 ['Interpret the measure within its limits.','A psychology model does not replace training.']);}

function lessonView(key,title,render,caption,terms){return {key,title,render,caption,terms};}
function personSituationModelFigure(){return scene('room','concept').replace('<svg ','<svg data-diagram="person-situation-model" ');}
const visualLessons={
 c01s03:[lessonView('person-situation-model','Person, disposition, and situation',personSituationModelFigure,'A disposition is one personal quality; circumstances also contribute.',['Disposition','Situation'])],
 c01s03b:[lessonView('person-situation','Disposition under changing demands',personSituationFigure,'A hypothetical interaction of a disposition and a situation. Dashed paths indicate possible contributions.',['Disposition'])],
 c01s04:[lessonView('observation-attribution','Observation and attribution',observationFigure,'Leo’s observation and his attribution answer different questions.',['Observation','Attribution'])],
 c01s04b:[lessonView('attribution-error','Fundamental attribution error',attributionErrorScene,'Leo gives personal qualities more weight than the circumstances.',['Fundamental attribution error'])],
 c01s05:[lessonView('actor-observer','Attribution and actor–observer differences',actorObserverFigure,'Hypothetical explanations by the same observer.',['Attribution','actor–observer differences'])],
 c01s05b:[lessonView('repeated-evidence','Test an explanation against evidence',repeatedEvidenceFigure,'Describe, compare, check, and revise. Apply the same steps to your own interpretations.',[])],
 c02s03:[lessonView('confounding','Confounding',confoundingScene,conceptCaptions.c02s03,['Confound']),lessonView('sampling-assignment','Random sampling and random assignment',samplingFigure,'Choosing the sample and assigning conditions answer different questions.',['Random assignment','Random sampling']),lessonView('correlation-causation','Correlation and causation',correlationFigure,'A shared pattern leaves multiple causes possible.',['Correlation'])],
 c02s04:[lessonView('effect-size','Effect size and uncertainty',differenceFigure,'Invented counts illustrate the size of a difference.',['percentage points']),lessonView('significance-importance','Statistical significance and practical importance',significanceFigure,'Model-based evidence and practical value are different questions.',['Statistical significance'])],
 c02s05:[lessonView('research-reliability','Preregistration, transparency, and replication',researchCycleFigure,'Plan, inspect, and independently repeat a sound comparison.',['Replication','Preregistration'])],
 c03s03:[lessonView('availability-base-rate','Availability heuristic, base rates, and denominators',availabilityFigure,'The invented whole record gives a vivid case its denominator.',['Availability heuristic','Base rate','Denominator'])],
 c03s04:[lessonView('confirmation-bias','Confirmation bias',confirmationBiasScene,conceptCaptions.c03s04,['Confirmation bias']),lessonView('motivated-reasoning','Motivated reasoning',motivatedReasoningFigure,'Maya’s desired outcome may shape how she judges the evidence.',['Motivated reasoning'])],
 c03s05:[lessonView('bias-evidence','Check a bias claim against evidence',biasCheckFigure,'Compare another person’s estimate with the record behind it.',[])],
 c04s03:[lessonView('cognitive-dissonance','Cognitive dissonance and cognitions',dissonanceFigure,'Inconsistency can motivate several different responses.',['Cognitive dissonance','Cognitions'])],
 c04s04:[lessonView('sunk-cost','Sunk cost effect and future consequences',sunkCostScene,conceptCaptions.c04s04,['Sunk cost','Sunk cost effect'])],
 c04s05:[lessonView('dissonance-evidence','A procedure, a prediction, and a theory',dissonanceEvidenceFigure,'The cited replication concerns a particular induced-compliance procedure.',['induced-compliance'])],
 c05s03:[lessonView('conformity-motives','Informational influence and normative influence',conformityMotivesScene,conceptCaptions.c05s03,['Informational influence','Normative influence'])],
 c05s04:[lessonView('compliance-obedience','Compliance and obedience',authorityFigure,'Authority can add pressure; it does not make resistance impossible.',['Compliance','Obedience']),lessonView('questioning-authority','Questioning an unsafe instruction',safetyVoiceFigure,'An agreed route makes a concern actionable.',[])],
 c05s05:[lessonView('study-context','Classic studies in context',classicStudiesFigure,'Task, setting, ethics, and variation limit generalization.',[])],
 c06s03:[lessonView('message-processing','Central and peripheral processing',processingFigure,'The same person can process different messages more or less carefully.',['Elaboration likelihood model','Central processing','Peripheral processing']),lessonView('attitude-evaluation','Attitudes and action',attitudeFigure,'An evaluation and an action are related but distinct.',['Attitude'])],
 c06s04:[lessonView('social-norms','Descriptive and injunctive norms',normsFigure,'Behavior and approval are different claims; both need evidence.',['Descriptive norm','Injunctive norm']),lessonView('honest-request','An honest, usable invitation',honestRequestFigure,'Support understanding and preserve meaningful choice.',[])],
 c06s05:[lessonView('persuasion-outcomes','Attention, understanding, and participation',persuasionOutcomesFigure,'Measure later outcomes rather than assuming them from clicks.',[])],
 c07s03:[lessonView('ingroup-favoritism','Social identity and in-group favoritism',identityFigure,'Group preference can produce unequal treatment.',['Social identity','In-group favoritism']),lessonView('shared-goal','A shared goal and workable arrangements',sharedGoalFigure,'Shared identity needs coordination, resources, and decision rights.',[])],
 c07s04:[lessonView('group-polarization','Group polarization and consensus',groupPolarizationScene,conceptCaptions.c07s04,['Group polarization']),lessonView('loafing-coordination','Social loafing and coordination loss',loafingCoordinationFigure,'Different processes require different remedies.',['Social loafing','Coordination loss'])],
 c07s05:[lessonView('groupthink','Groupthink and visible decision processes',groupthinkFigure,'Ask members about their concerns and check which information reached the discussion.',['Groupthink'])],
 c08s03:[lessonView('belief-attitude-action','Stereotypes, prejudice, and discrimination',prejudiceFigure,'Belief, attitude, and action are related but distinct.',['Stereotype','Prejudice','Discrimination']),lessonView('structural-barriers','Rules and unequal access',structuralBarrierFigure,'An arrangement can exclude without an openly hostile statement.',[])],
 c08s04:[lessonView('intergroup-contact','Intergroup contact and participation',contactFigure,'Cooperation, equal status, shared goals, and support matter.',['Intergroup contact']),lessonView('procedural-change','Procedural changes to access',proceduralChangeFigure,'Examine who can enter and participate after the change.',['Procedural change'])],
 c08s05:[lessonView('attitude-measures','Explicit attitudes, implicit associations, and behavior',prejudiceMeasuresFigure,'Different measurements do not supply a complete character diagnosis.',['explicit attitude','implicit association'])],
 c09s03:[lessonView('relationship-opportunity','Proximity and similarity',opportunityFigure,'Shared settings create opportunities, with mutual willingness.',['Proximity','Similarity']),lessonView('mere-exposure','The mere exposure effect',exposureFigure,'Familiarity has limits and does not override boundaries.',['Mere exposure effect'])],
 c09s04:[lessonView('disclosure-responsiveness','Disclosure, responsiveness, and reciprocity',responsivenessFigure,'Connection depends on what each person wants and how the other responds.',['Disclosure','Responsiveness','Reciprocity']),lessonView('attachment-boundary','Attachment labels and stated boundaries',attachmentBoundaryFigure,'Leo can respect Sam’s preference without inferring an attachment style.',['Attachment'])],
 c09s05:[lessonView('relationship-evidence','Relationship evidence and its limits',relationshipEvidenceFigure,'Use research to frame questions, then ask about Sam and Leo’s own experiences and preferences.',[])],
 c10s03:[lessonView('helping-barriers','Helping and the bystander effect',helpingBarriersScene,'In some settings, others’ presence can reduce an individual’s likelihood of helping. These are two possible processes; context, skills, and support also matter.',['Bystander effect','Diffusion of responsibility','Pluralistic ignorance']),lessonView('helping-path','A safe helping process',helpingPathFigure,'Clear responsibility, skills, and support can make action feasible.',[])],
 c10s04:[lessonView('anger-aggression','Anger, aggression, and de-escalation',aggressionFigure,'A feeling does not predetermine a harmful action.',['Aggression','De-escalation']),lessonView('cooperation-plan','Cooperation with roles and feedback',cooperationFigure,'A specific arrangement can turn a shared aim into coordinated work.',['Cooperation'])],
 c10s05:[lessonView('proxy-and-context','Research measures, context, and safe help',proxyMeasuresFigure,'Interpret controlled tasks and real incidents with appropriate limits.',[])]
};
