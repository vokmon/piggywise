# PiggyWise (หมูทอง)

**ระบบบริหารพอร์ตโฟลิโออัจฉริยะด้วย AI สำหรับนักลงทุนชาวไทย**

PiggyWise ขาย Google Sheets template ที่ทำหน้าที่เป็นโค้ชการเงินส่วนตัว: DCA รายเดือนอัตโนมัติ, ระบบปรับสมดุล, และคลัง AI Prompt ที่เปลี่ยน AI ใดก็ได้ให้เป็นที่ปรึกษาการเงินส่วนตัว ข้อมูลทั้งหมดอยู่ใน Google Drive ของลูกค้า — PiggyWise ไม่มี backend

---

## เอกสารหลัก

- [`docs/PRODUCTS.md`](docs/PRODUCTS.md) — **ข้อมูลสินค้าทั้งหมด** (single source of truth): สินค้า 4 รายการ, ฟีเจอร์, ราคา, copy EN/TH, ข้อห้ามในงานเขียน
- [`docs/PiggyWise_master_blueprint.md`](docs/PiggyWise_master_blueprint.md) — พิมพ์เขียวธุรกิจฉบับเต็ม: กลยุทธ์ GTM, การตั้งราคา, checklist ดำเนินงาน

---

## โครงสร้าง Repo

```
scripts/
  generate_covers.py     # สร้าง cover 8 ภาพ (4 สินค้า × 2 ภาษา)
  generate_slides.py     # สร้าง slides 20 ภาพ (slides 1–7 × EN/TH)

images/
  bg/                    # background สำหรับ cover (1 ไฟล์ต่อ product key)
  bg/slides/             # background สำหรับ shared slides
  cover/                 # output: cover images
  slides/                # output: slide images
  logo/                  # โลโก้และ icon

docs/
  PRODUCTS.md            # ข้อมูลสินค้า (single source of truth)
  PiggyWise_master_blueprint.md  # พิมพ์เขียวธุรกิจ (ภาษาไทย)
```

---

## Brand

| องค์ประกอบ | ค่า |
|-----------|-----|
| Background | `#0D0D0D` |
| Gold (accent) | `#D4A017` |
| White (primary text) | `#FFFFFF` |
| Off-White (secondary text) | `#E8E0D0` |
| Dark Surface (cards) | `#1A1A1A` |
| โทนเสียง | Ultra premium — ระดับ Amex Black / Porsche |
| ภาษาหลัก | ภาษาไทยมาก่อนในทุก customer-facing material |
| Font (EN) | Avenir Next Heavy — ใช้ทั้งหมด |
| Font (TH) | Krungthep — ใช้ทั้งหมด |
