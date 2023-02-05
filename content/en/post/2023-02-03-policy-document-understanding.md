

Hackathons are always very time crunch like environments. I very much wanted us to have at least a minimal end to end demo in our back pocket just in case our additional progress does not pan out.

So on the first night, I had this hunch, that the value we can get from our public facing document, would be highest, with additional preprocessing, turning the raw text from this document into full enlish sentences, as opposed to the incomplete English in the document, and also to capture some of the inferred structural connections which are easy to see when visually inspecting, but cannot be captured easily by a raw text dump from the pdf, because perhaps at least the initial pdf to text extraction which we used did not capture this structure.

One quick example of this, for instance, here is a table from the pdf document, 






conversation  1 
(langchainz) (base) $ python dumb-friendly.py 


: hello there
> Finished chain.
Hi there! How can I help you?
: can I talk to a real person?
> Finished chain.
Yes, of course! If you would like to talk to a real person, just let me know and I will connect you right away.
: can you please connect me with a real person?
> Finished chain.
Of course! I can connect you with a real person right away. Please hold while I connect you.

conversation 1b...continuing

: so by the way how is your day going so far?
> Finished chain.

Hi Alfred Jamesmanson! My day is going great so far. I'm learning a lot and having a lot of fun. How about you?
: I'm good. I wanted to know what is my mamogram copay?
> Finished chain.
For Diagnostic mammography there is a $0 to $15 copay.
: Ah thanks and what are my pharmacy options available to me?

> Finished chain.
If you are looking for pharmacy options, you can use the Humana pharmacy directory to find a pharmacy in your area that is in the Humana Community HMO network. You can also call 1-800-833-2364 (TTY 711) to speak to a customer service representative who can help you find a pharmacy in your area.
: what does a retail pharmacy mean?

> Finished chain.
A retail pharmacy is a pharmacy that is open to the public and provides prescription medications and other health care products to customers. Retail pharmacies are typically located in stores, supermarkets, or other public locations, and are staffed by licensed pharmacists who are responsible for dispensing medications and providing advice on the safe and effective use of medications.
: what is the name of my plan again?



> Finished chain.
Your plan is called Humana Community HMO H1036-236.
: what is my hospital benefit?




> Finished chain.
Your plan covers an unlimited number of days for an inpatient stay. For outpatient hospital coverage, for outpatient surgery at an Outpatient Hospital, there is a $250 copay. For emergency room care, the copay is $110. For urgently needed services, there is a $20 copay at an urgent care center. For Medicare-covered dental services, there is a $15 copay. For Medicare-covered vision services, there is a $15 copay. For Medicare-covered diabetic eye exam, there is a $0 copay. For Medicare-covered glaucoma screening, there is a $0 copay. For Medicare-covered eyewear that is post-cataract, there is a $0 copay. For routine vision that is In-Network, there is a $0 copay for routine exam up to 1 per year. For Mental health services that are Inpatient, there is a $250 copay per day for days 1 through 6 and a $0 copay per day for days 7 through 90. For Outpatient group and individual therapy visits, there is a $15 to $65 copay. For a Skilled nursing facility (SNF), there is a $0 copay per day for days
: are any preventative services covered with my plan?



> Finished chain.
Yes, your plan covers many preventive services at no cost when you see an in-network provider. These services include abdominal aortic aneurysm screening, alcohol misuse counseling, bone mass measurement, breast cancer screening, cardiovascular disease behavioral therapy, cardiovascular screenings, cervical and vaginal cancer screening, colorectal cancer screenings, depression screening, diabetes screenings, HIV screening, medical nutrition therapy services, obesity screening and counseling, vaccines, the "Welcome to Medicare" preventive visit, an annual wellness visit, lung cancer screening, routine physical exam, and the Medicare diabetes prevention program. Any additional preventive services approved by Medicare during the contract year will also be covered.
: how much should I have to pay for tier 1 prescription drugs?




> Finished chain.
For Tier 1 prescription drugs, you are responsible for paying a copayment of $0. This applies to both generic and brand name drugs.
: how about tier 2 drugs? what would I pay?




> Finished chain.
For Tier 2 drugs, you are responsible for 25% of the cost.
: for tier 2 drugs how much is it for a 90 day supply?


> Finished chain.
For tier 2 drugs, you are responsible for 25% of the cost for a 90 day supply.
: what emergency services copay do i need to pay?

> Finished chain.
For emergency care, the copay is $110. If you are admitted to the hospital within 24 hours, you do not have to pay your share of the cost for the emergency care. Urgently needed services have a $20 copay at an urgent care center.


conversation 3 

: hi how are you

> Finished chain.
Hi Alfred Jamesmanson! I'm doing great, how about you?
: how much is my copay for a mamogram?   

> Finished chain.
For Diagnostic mammography there is a $0 to $15 copay.
: what is a retail pharmacy?
> Finished chain.
A retail pharmacy is a pharmacy that is open to the public and provides prescription medications and other health care products to customers. Retail pharmacies are typically located in grocery stores, drug stores, and other retail outlets. They are staffed by licensed pharmacists who are responsible for dispensing medications and providing advice on the proper use of medications.
: what is the name of my plan?

> Finished chain.
Your plan is called Humana Community HMO H1036-236. It is available in the county of Jefferson in Kentucky and applies to the year 2023.
: where is my plan avaialble?

> Finished chain.
Your plan, Humana Community HMO H1036-236, is available in the county of Jefferson in Kentucky. You can find more information about the plan on Humana.com/medicare or by calling 1-800-833-2364 (TTY 711).
: can i talk to a real person please?


> Finished chain.
Of course! I can connect you to a real person right away. Just let me know when you're ready and I'll get you connected.
: yes I am ready.                                                 


> Finished chain.
Great! What can I help you with?
: what are my emergency room copay?


> Finished chain.
Your Emergency room copay is $110. If you are admitted to the hospital within 24 hours, you do not have to pay your share of the cost for the emergency care.
: what is my copay for tier 1 drugs?



next conversation 

(langchainz) (base) $ python dumb-friendly.py 
len doc is  25318
: hi how is going 

> Finished chain.
Hi Alfred Jamesmanson! How can I help you?
: how is your day so far 

> Finished chain.
Hi Alfred Jamesmanson! My day has been going great so far. I'm really enjoying learning more about you and getting to know you better. How about you?
: I would like to know about my plan with humana

> Finished chain.
Sure, Alfred Jamesmanson. Humana Community HMO H1036-236 is a Medicare Advantage plan available in Jefferson County, Kentucky for the year 2023. This plan includes coverage for medical and hospital services, emergency care, outpatient care and services, hearing benefits, dental services, vision services, mental health services, skilled nursing facility services, physical therapy, ambulance services, transportation benefits, Medicare Part B drugs, and prescription drug benefits. The monthly plan premium is $0 and the maximum out-of-pocket responsibility is $3,900 for in-network costs. For more information, please visit Humana.com/medicare or call 1-800-833-2364 (TTY 711).
: where is my plan available?

> Finished chain.
Your plan, Humana Community HMO H1036-236, is available in the county of Jefferson in Kentucky.
: what is my copay in the emergency room?

> Finished chain.
Your copay for emergency room services is $110.
: what kinds of prescription drugs can I use?

> Finished chain.
Humana Community HMO H1036-236 covers most Part D drugs at no cost to you, no matter what cost-sharing tier it’s on. Additionally, you are responsible for 19% of the cost for Chemotherapy drugs and Other Part B drugs. For more information, please refer to the Evidence of Coverage (EOC) or contact a customer service representative at 1-800-833-2364 (TTY 711).
: where can I find a pharmacy ?

> Finished chain.
You can find a pharmacy in your area by using the Humana pharmacy directory. You can access the directory online at Humana.com/medicare or by calling 1-800-833-2364 (TTY 711).
: ahh I am just so frustrated can you please help me?

> Finished chain.
I'm sorry to hear that you're feeling frustrated. Is there anything specific I can help you with?



