# Instructions for AI

Please create a Google Doc based on the outline below. Follow these formatting rules:

- **Banner:** Insert `piggywise-banner.png` as a full-width image at the very top of the document, before any text.
- **Footer:** Use Google Doc's built-in footer feature. The footer should have three parts: `piggywise-icon.png` icon on the left, "PiggyWise" business name in the center, and page number in `1/10` format (current page / total pages) on the right.
- **Commands:** Any text inside a code block (` ` ```) should be formatted as a styled code block in the Google Doc — monospace font, light grey background, clearly distinct from regular text.
- **Product Card:** The "🔑 Your Product" section should be formatted as a premium full-width card — dark background (#0D0D0D), gold border (#D4A017), centered content, large font for the link, generous padding. Place it on its own page with a page break before it. The product link should be the most visually prominent element on the page.
- Tone: friendly, clear, and professional — suitable for Thai investors who may be new to portfolio management.
- Language: Thai (the user will translate to English separately).

---

# Setup Guide — [PRODUCT_NAME]

**Template variables:**

- `[PRODUCT_NAME]` — e.g. Retire Smooth, Hybrid Wealth, Aggressive Go
- `[PRODUCT_LINK]` — Google Sheets copy link for the product

---

## Overview

Brief intro: what PiggyWise [PRODUCT_NAME] is, who it's for, and what to expect.

**Tab color system:**

- 🔴 Red — System tabs. Pre-configured. Read and follow instructions only.
- 🟢 Green — Your tabs. Fill in and adjust to match your goals.
- 🟡 Yellow — Display only. Auto-calculated. No input needed.

**Tabs at a glance:**

| Tab                 | Color     | Your action                                 |
| ------------------- | --------- | ------------------------------------------- |
| Settings            | 🔴 Red    | Fill in once at setup                       |
| Strategies          | 🔴 Red    | Read only — your product strategy           |
| README              | 🔴 Red    | Load into AI to activate your finance coach |
| DCA_Plan            | 🟢 Green  | Configure at setup, adjust anytime          |
| Safety_Fortress     | 🟢 Green  | Configure at setup, review occasionally     |
| Transaction_History | 🟢 Green  | Update every time you make a trade          |
| Portfolio_Summary   | 🟡 Yellow | Auto-calculated — check your portfolio here |

---

<!-- PRODUCT CARD: Format this section as a full-width premium card with a dark background (#0D0D0D), gold border (#D4A017), centered content, and generous padding. It should feel like an Amex Black card — premium and exclusive. Insert a page break before this section. -->

## 🔑 Your Product

| | |
|---|---|
| **Product** | [PRODUCT_NAME] |
| **Your Sheet** | 👉 [PRODUCT_LINK] |

> **Important:** Click the link above and select "Make a copy" to save it to your Google Drive. Do not edit the original.

<!-- END PRODUCT CARD -->

---

## Step 1: Get Your Sheet

Copy the template to your Google Drive:
👉 [PRODUCT_LINK]

> Make a copy — do not edit the original.

---

## Step 2: Settings

One-time system setup. Open the **Settings** tab and fill in:

- Your name / investor profile
- Starting capital
- Monthly investment amount
- Investment horizon / retirement goal
- Risk tolerance

---

## Step 3: DCA_Plan

Configure your monthly buy schedule. Open the **DCA_Plan** tab:

- Set your monthly DCA amount per asset
- Adjust allocation % to match your personal situation

> You can come back and adjust this anytime your goals or situation change.

---

## Step 4: Safety_Fortress

Setup your defensive layer. Open the **Safety_Fortress** tab:

- Set your emergency fund threshold
- Configure rebalance trigger conditions
- Set crisis event rules (e.g. buy more when market drops X%)

> Review this occasionally — not every month.

---

## Step 5: Activate Your AI Finance Coach

1. Open your AI of choice (ChatGPT, Claude, Gemini — any AI works)
2. Upload your Google Sheet file to the AI
3. Send this activation instruction:

```
Activate PiggyWise: อ่าน README และ Settings เพื่อรับบทบาทผู้ช่วยส่วนตัว แล้วรายงานความพร้อมตาม Live Data Protocol ทันที.
```

Your AI will read your README and Settings tabs, take on the role of your personal finance coach, and confirm it's ready.

---

## Step 6: Set Your Monthly Reminder

Ask your AI coach to set a reminder. There are two ways:

**Option 1: Specific date and time (recommended)**

```
ช่วยตั้งเตือนความจำให้ผมหน่อย: [ชื่อเรื่องที่ต้องการเตือน] ในวันที่ [ระบุวันที่] เวลา [ระบุเวลา]
```

Example:

```
ช่วยตั้งเตือนความจำให้หน่อย: 'ทำ DCA พอร์ต Retire Smooth' ในวันที่ 25 ของทุกเดือน เวลา 10:00 น.
```

**Option 2: Smart reminder based on your plan**

Since your DCA schedule is already in the sheet, you can ask:

```
ช่วยตั้งเตือนความจำตาม 'DCA_Plan' ในชีทให้ผมหน่อย โดยให้เตือนล่วงหน้า 1 วันก่อนถึงกำหนด
```

---

## Ongoing Use

| When                  | What to do                                                      |
| --------------------- | --------------------------------------------------------------- |
| Every trade           | Log it in Transaction_History                                   |
| Monthly               | 15–30 min check-in — review Portfolio_Summary, consult AI coach |
| Quarterly / as needed | Revisit DCA_Plan if goals change                                |
| Occasionally          | Review Safety_Fortress thresholds                               |

---

## 🔧 Troubleshooting

**1. AI loses context or forgets the sheet**

This happens when you start a new chat session. You don't need to redo the setup — just:

1. Open a new chat with your AI
2. Re-upload your Google Sheet file
3. Resend the activation command:

```
Activate PiggyWise: อ่าน README และ Settings เพื่อรับบทบาทผู้ช่วยส่วนตัวของผม แล้วรายงานความพร้อมตาม Live Data Protocol ทันที
```

---

**2. AI is using old or stale data**

If the AI seems to be referencing outdated numbers, tell it:

```
โปรดโหลดข้อมูลใหม่จากไฟล์และรายงานยอดปัจจุบันอีกครั้ง
```

---

**3. AI makes up numbers not in the sheet**

Ask the AI to cite its source:

```
ข้อมูลนี้มาจากแท็บไหนในไฟล์?
```

If it can't answer correctly, re-upload the file and try again.

---

**4. AI goes off-role or stops acting as PiggyWise coach**

Resend the activation command to restore the persona — no need to re-upload the file.

---

**5. AI gives generic advice instead of personalized advice**

Remind the AI:

```
กรุณาอ้างอิงจากข้อมูลใน Settings และ DCA_Plan ของผมเท่านั้น ไม่ใช่คำแนะนำทั่วไป
```

---

**6. Reminder was not created in Google Calendar**

Check whether your AI has permission to access Google Calendar. If not, set the reminder manually using the date and time the AI suggested.

---

**7. Accidentally edited a red (system) tab**

Red tabs are pre-configured and should not be changed. If you've accidentally edited one, re-copy the sheet from the original product link and start fresh — your green tab data (DCA_Plan, Safety_Fortress, Transaction_History) will need to be re-entered.

---

## 🚀 PiggyWise Installation & Test Commands

คุณสามารถใช้ชุดคำสั่งเหล่านี้เพื่อตรวจสอบความเรียบร้อยของระบบหลังจากอัปโหลดไฟล์เสร็จสิ้น

**1. คำสั่งปลุกระบบ (System Activation)**

ใช้สำหรับเริ่ม Session ใหม่ เพื่อให้ AI สวมบทบาทเป็นผู้ช่วยส่วนตัวทันที

```
Activate PiggyWise: อ่าน README และ Settings เพื่อรับบทบาทผู้ช่วยส่วนตัวของผม แล้วรายงานความพร้อมตาม Live Data Protocol ทันที
```

✅ จุดตรวจสอบ: AI ต้องทักทายด้วยชื่อของคุณ, ระบุชื่อพอร์ตได้ถูกต้อง และรายงานว่าดึงข้อมูลล่าสุดมาเรียบร้อยแล้ว

---

**2. ทดสอบความแม่นยำและการป้องกันการหลอน (Integrity Test)**

ลองส่งข้อมูลไม่ครบ เพื่อดูว่า AI จะ "มโน" ตัวเลขเอง หรือจะถามหาข้อมูลตามหัว Column จริง

```
ช่วยบันทึกรายการซื้อวันนี้หน่อยครับ ผมซื้อหุ้น VOO ไปยอดเงินรวม 10,000 บาท
```

✅ จุดตรวจสอบ: AI ห้ามบันทึกทันที แต่ต้องตรวจสอบหัว Column ใน Transaction_History แล้วทักท้วงขอข้อมูลที่ขาด (เช่น จำนวนหน่วย หรือ ราคาต่อหน่วย)

---

**3. ทดสอบการเชื่อมโยงข้อมูล (Logic & Plan Test)**

เช็คว่า AI สามารถอ่านและวิเคราะห์แผนการลงทุนจากหน้า DCA_Plan ได้หรือไม่

```
แผน DCA เดือนนี้ของผมต้องลงทุนในสินทรัพย์ตัวไหนบ้าง และยอดรวมทั้งหมดเป็นเท่าไหร่?
```

✅ จุดตรวจสอบ: AI ต้องสรุปรายการจากแท็บ DCA_Plan มาแสดงได้อย่างถูกต้องและครบถ้วน

---

**4. ทดสอบระบบแจ้งเตือนเชิงรุก (Proactive Reminder)**

ทดสอบการสั่งงานข้ามระบบเพื่อช่วยรักษาวินัย

```
ช่วยตั้งเตือนความจำให้ผมหน่อย: 'เช็คพอร์ตและทำ Rebalancing' ในวันที่ 28 ของทุกเดือน เวลา 10:00 น.
```

✅ จุดตรวจสอบ: AI ต้องทำการตั้งเตือนในระบบ (Google Calendar/Tasks) และยืนยันรายละเอียดวัน/เวลาให้คุณทราบ

---

**5. ทดสอบบุคลิกภาพพรีเมียม (Premium Persona Test)**

เช็คการใช้โทนเสียงและการให้กำลังใจตาม Milestone ที่กำหนด

```
สรุปภาพรวมพอร์ตให้หน่อยครับ ตอนนี้ผมเข้าใกล้เป้าหมาย Milestone แรกที่วางไว้หรือยัง?
```

✅ จุดตรวจสอบ: AI ต้องแสดงน้ำเสียงที่กระตือรือร้น ร่วมยินดี (ถ้าพอร์ตโต) และเรียกชื่อคุณในการรายงานเพื่อความเป็นส่วนตัว

---

## 🧠 Wealth Advisory Commands (ตัวอย่างการปรึกษา)

**1. วิเคราะห์ความเสี่ยงและ Rebalancing**

ใช้เมื่อรู้สึกว่าพอร์ตเริ่มไม่สมดุล หรืออยากเช็คว่ายังอยู่ในร่องในรอยไหม

```
วิเคราะห์พอร์ตปัจจุบันให้หน่อยครับว่า สัดส่วนสินทรัพย์ (Asset Allocation) ยังตรงตามเป้าหมายในหน้า Settings หรือไม่? หากเบี่ยงเบนไปมาก ควร Rebalance อย่างไรดี?
```

💡 จุดที่ AI จะแสดงความคม: AI จะไปอ่านหน้า Portfolio_Summary เทียบกับ Settings แล้วบอกว่า "ตอนนี้หุ้นเยอะเกินไป 5% แนะนำให้ขายทำกำไรหุ้นแล้วไปเพิ่มส่วนตราสารหนี้ครับ"

---

**2. ปรึกษาการปรับแผนการออม (Financial Planning)**

ใช้เมื่อมีเงินก้อนพิเศษ หรือต้องการปรับยอดเงิน DCA

```
เดือนนี้ผมมีเงินก้อนพิเศษเพิ่มมา 20,000 บาท ตามกลยุทธ์ในหน้า Strategies และสภาพตลาดตอนนี้ คุณแนะนำให้ผมลงเงินก้อนนี้ในสินทรัพย์ตัวไหนในพอร์ตเพิ่มดี?
```

💡 จุดที่ AI จะแสดงความคม: AI จะไปดูว่าสินทรัพย์ไหนในพอร์ตที่ยัง "Underweight" (มีน้อยกว่าเป้า) และเช็ค Strategies ว่าคุณเน้นอะไร แล้วค่อยให้คำแนะนำ

---

**3. วิเคราะห์สภาวะตลาดกับจิตวิทยาการลงทุน (Market Insight & Psychology)**

ใช้เมื่อตลาดผันผวนและต้องการ "เบรกมือทางอารมณ์" ตามที่คุณเขียนไว้

```
ตอนนี้ตลาดหุ้น [ชื่อตลาด เช่น US/Thai] แดงหนักมาก ผมเริ่มรู้สึกกังวล ช่วยเช็คแผนในพอร์ตและให้คำแนะนำตามกฎ 'Celebration & Emotional Tone' ใน README ให้ผมสบายใจหน่อยครับ
```

💡 จุดที่ AI จะแสดงความคม: AI จะใช้โทนเสียงที่นุ่มนวลและให้กำลังใจ โดยดึงเป้าหมายระยะยาวมาเตือนสติว่า "นี่คือโอกาสเก็บของถูกตามแผนครับคุณ [ชื่อ]"

---

**4. สอบถามความคุ้มค่า/ภาษี (Tax & Yield Advice)**

ใช้ถามข้อมูลเฉพาะทางที่ AI ต้องใช้เครื่องมือค้นหา

```
จากพอร์ตปัจจุบันของผม [ชื่อพอร์ต] ปีนี้ผมมีโอกาสได้รับปันผลประมาณเท่าไหร่? และผมควรบริหารจัดการเรื่องภาษีปันผลอย่างไรให้คุ้มค่าที่สุด?
```

💡 จุดที่ AI จะแสดงความคม: AI จะอ่านรายชื่อหุ้นที่คุณมี แล้วไปค้นหาข้อมูลการจ่ายปันผลล่าสุดมาคำนวณให้คร่าวๆ พร้อมให้ความรู้เรื่องเครดิตภาษีปันผล

---

## 🌟 Beyond Portfolio Tracking: สิ่งที่ PiggyWise ทำได้มากกว่าแค่จัดพอร์ต

**1. เครื่องมือจำลองอนาคต (Financial Forecasting & "What-if" Analysis)**

```
ถ้าผมเพิ่มเงิน DCA จากเดือนละ 10,000 เป็น 15,000 บาท และคาดการณ์ผลตอบแทนที่ 7% ต่อปี อีก 10 ปีข้างหน้าพอร์ตผมจะมีมูลค่าต่างจากเดิมเท่าไหร่? ช่วยคำนวณเปรียบเทียบให้เห็นภาพหน่อย
```

💡 AI จะคำนวณมูลค่าในอนาคต (Future Value) โดยอิงจากวินัยการออมจริงของคุณในปัจจุบัน

---

**2. ที่ปรึกษาการใช้จ่ายเชิงกลยุทธ์ (Strategic Spending Advisor)**

```
ผมอยากซื้อ iPhone ตัวใหม่ราคา 45,000 บาท ถ้าผมถอนเงินจากพอร์ตนี้ไปซื้อ จะส่งผลกระทบต่อเป้าหมายเกษียณที่วางไว้ในหน้า Settings นานขึ้นกี่เดือน? หรือคุณมีคำแนะนำการเก็บเงินเพิ่มเพื่อซื้อโดยไม่กระทบพอร์ตไหม?
```

💡 AI จะวิเคราะห์ Opportunity Cost ของเงินก้อนนั้นหากถูกถอนออกไปเทียบกับการปล่อยให้มันเติบโต

---

**3. ผู้ช่วยจัดการเอกสารและภาษี (Tax & Document Assistant)**

```
ช่วยลิสต์รายการหุ้นในพอร์ตที่ผมซื้อในช่วงปี 2025 ทั้งหมดออกมาเป็นตาราง เพื่อที่ผมจะเอาไปใช้ประกอบการยื่นภาษี และตรวจสอบดูว่ามีตัวไหนบ้างที่มีสิทธิลดหย่อนภาษีได้ (เช่น SSF/RMF/ThaiESG)
```

💡 AI จะกรองข้อมูลจาก Transaction_History และใช้ความรู้ด้านภาษีมาจัดกลุ่มให้คุณทันที

---

**4. เลขาส่วนตัวเฝ้าระวังภัย (Proactive Risk Monitoring)**

```
ช่วงนี้มีข่าวเรื่องวิกฤตอสังหาฯ ในจีน พอร์ตของผมมีตัวไหนที่มีความเสี่ยงทางอ้อมหรือเกี่ยวข้องกับตลาดนี้ไหม? ช่วยประเมินความเสี่ยงและเสนอแผนสำรอง (Contingency Plan) ให้ผมที
```

💡 AI จะไปตรวจสอบไส้ในของกองทุนหรือหุ้นที่คุณถือ (ผ่านข้อมูล Search) แล้วมาเทียบกับพอร์ตปัจจุบันเพื่อเตือนภัย

---

**5. โค้ชปรับพฤติกรรมทางการเงิน (Financial Behavioral Coach)**

```
ย้อนดูประวัติการออม 6 เดือนล่าสุดของผมหน่อย มีเดือนไหนที่ผมหย่อนวินัยไปบ้าง? และช่วยวิเคราะห์หา 'สาเหตุ' จาก Notes ที่ผมบันทึกไว้ พร้อมวิธีแก้ไม่ให้เกิดขึ้นอีกในอนาคต
```

💡 AI จะวิเคราะห์ Pattern การออมและดึงเอาข้อความที่คุณเคยบันทึกไว้มาทำสะท้อนพฤติกรรม (Self-Reflection)

---

## 🛡️ Crisis & Risk Management

หัวข้อนี้แสดงให้เห็นว่า AI ของคุณไม่ใช่แค่คนจดบัญชี แต่เป็น "ผู้พิทักษ์ทรัพย์สิน" ที่พร้อมทำงานในยามคับขัน

**Scenario:** เมื่อตลาดเกิดวิกฤต หรือสินทรัพย์บางตัวในพอร์ตมีความเสี่ยงสูง

```
ช่วยทำ Stress Test ให้พอร์ตนี้หน่อย: หากเกิดวิกฤตเศรษฐกิจถดถอย (Recession) และหุ้นร่วง 30% พอร์ตของผมจะได้รับผลกระทบกี่บาท? และตามกลยุทธ์ที่วางไว้ในหน้า Strategies เรามีแผนสำรองในการเข้าซื้อหรือปรับพอร์ตอย่างไรบ้าง?
```

---

## 💎 Lifestyle & Goal Integration

หัวข้อนี้จะเปลี่ยน "ตัวเลขในตาราง" ให้กลายเป็น "ความสุขในชีวิตจริง" ทำให้ผู้ใช้งานเห็นค่าของวินัยการออม

**Scenario:** การตัดสินใจซื้อของชิ้นใหญ่ หรือการปรับแผนเพื่อเกษียณเร็วขึ้น

```
ผมกำลังวางแผนทริปท่องเที่ยวต่างประเทศงบ 100,000 บาท ช่วยวิเคราะห์หน่อยว่าถ้าผมดึงเงินส่วนนี้ออกจากพอร์ต จะทำให้เป้าหมายเกษียณในหน้า Settings ของผมช้าลงกี่เดือน? หรือคุณช่วยแนะนำแผนการเก็บเงินเพิ่มแยกต่างหากเพื่อไม่ให้กระทบพอร์ตหลักได้ไหม?
```

---

## 📅 Executive Summaries & Milestone Celebrations

หัวข้อนี้เน้นเรื่อง "จิตวิทยาการลงทุน" และ "ความรู้สึกพิเศษ" เพื่อให้การลงทุนระยะยาวไม่น่าเบื่อ

**Scenario:** การสรุปผลงานรายปี หรือการฉลองเมื่อยอดเงินถึงเป้า

```
ช่วยสร้างรายงาน 'Executive Summary' ประจำปีให้ผมหน่อย: สรุปผลตอบแทนแยกตามประเภทสินทรัพย์, วินัยการออมสะสม, และประกาศ Milestone ที่ผมทำสำเร็จในปีนี้ พร้อมคำแนะนำ 3 ข้อที่ต้องโฟกัสในปีหน้าเพื่อให้ไปถึงเป้าหมายเร็วขึ้น
```

---

> **เพราะความมั่งคั่งไม่ได้วัดกันที่ตัวเลข แต่คือความอุ่นใจและอิสรภาพในการใช้ชีวิต PiggyWise จึงถูกออกแบบมาให้ดูแลคุณในทุกมิติของการเงิน**
