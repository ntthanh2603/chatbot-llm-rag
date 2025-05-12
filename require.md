##### Các yêu cầu của dự án

- Xây dựng hệ thống có thể trả lời các câu hỏi. Bạn có thể làm nhiệm vụ trả lời các câu hỏi thực tế(QA). Vì các hệ thống QA hiện tại có thể không đủ kiến thức cần thiết trong lĩnh vực này, bạn sẽ cần bổ xung thêm các dữ liệu có liên quan vào mỗi câu hỏi. Với mỗi câu hỏi đầu vào, hệ thống của bạn sẽ lấy các tài liệu và sử dụng các tài liệu đó để tạo ra câu trả lời.
- Bạn phải thu thập dữ liệu của riêng mình và phát triển một mô hình theo lựa chọn của bạn trên dữ liệu này. Bạn sẽ chạy hệ thống đã xây dựng của mình trên dữ liệu này để gửi kết quả. Chúng tôi cũng yêu cầu bạn làm theo một số phương pháp hay nhất trong thử nghiệm và mô tả kêts quả trong báo cáo của bạn.

###### Định dạng dữ liệu

- Tập questions.txt một tệp văn bản chứa 1 câu hỏi trên 1 dòng.
- Tệp system_output.txt một tệp văn bản chứa các câu trả do hệ thống tạo ra. Mỗi dòng chứa một chuỗi các câu trả lời duy nhất do hệ thống của bạn tạo ra tương ứng với câu hỏi trong questions.txt.
- Tệp reference_answers.txt một tập văn bản chứa các câu trả lờiời tham khảo. Mỗi dòng chứa 1 hoặc nhiều câu trả lời tham khảo tương ứng với tập questions.txt.

###### Chuẩn bị dữ liệu thô

- Biên soạn 1 nguồn kiến thức: Được dùng bộ dữ liệu công khai nhưng nên dùng tài liệu từ các trang web có tài liệu như:

  - Giới thiệu chung về lịch sử của VNU:
    - Trang web chính thức của đại học quốc gia Hà Nội: Cung cấp về thông tin tổng quan lịch sử, cơ cấu tổ chức và sứ mệnh của nhà trường.
    - Trang wikipedia về VNU: Cung cấp thông tin chi tiết về quá trình thành cập và phát triển của trường trường theo thời gian.
  - Thông tin tuyển sinh:
    - Cổng thông tin tuyển sinh của VNU: Bao gồm các thông tin về chương trình học thuật, thủ tục tuyển sinh và yêu cầu đào tạo,
    - Thông báo về các trường đại học thành viên, ví dụ: USSH, ULIS, UET, HUS.
  - Quy định học thuật:
    - Chương trình đào tạo chung: Danh mục các chương trình đào tạo đại học, thạc sĩ, tiến sĩ được đào tạo tại VNU.
    - Chương trình đào tạo quốc tế: Thông tin về các chương trình đào tạo liên kết đối tác quốc tế và các chương trình giảng dạy bằng tiếng anh.

- Thu thập dữ liệu thô:
  - Để xử lý các trang HTML có thể dùng beautifulsoup4v.
  - Để xử lý các tệp PDF có thể dùng pypdf hoặc pdfplumber.

###### Chú thích dữ liệu

Chú thích các cặp câu hỏi, câu trả lời cho 2 mục đích là train và test. Sử dụng tài liệu đã biên soạn trước đó để xác định các câu hỏi cho chú thích.

- Dữ liệu thử nghiệm là dữ liệu đảm bảo hệ thống đang hoạt động bình thường. Để làm như vậy, bạn sẽ muốn chú thích đủ dữ liệu để có thể ước tính chính xác về cách hệ thống của bạn đang hoạt động và liệu bất kỳ cải tiến nào đối với hệ thống của bạn có tác động tích cực hay không. Một số hướng dẫn về điều này:
  - Để làm như vậy, bạn sẽ muốn chú thích đủ dữ liệu để có thể ước tính chính xác về cách hệ thống của bạn đang hoạt động và liệu bất kỳ cải tiến nào đối với hệ thống của bạn có tác động tích cực hay không. Một số hướng dẫn về điều này
  - Tính đa dạng: Dữ liệu kiểm tra của bạn phải bao gồm nhiều câu hỏi của UET và VNU.
  - Kích thước: Dữ liệu thử nghiệm của bạn phải đủ lớn để phân biệt giữa các mô hình tốt và xấu.
  - Chất lượng: Dữ liệu thử nghiệm của bạn phải có chất lượng cao. Chúng tôi khuyên bạn nên tự chú thích và
    xác thực chú thích của mình trong nhóm của bạn.
  - Đây là 1 số ví dụ:
    - Những câu hỏi có thể được trả lời chỉ bằng cách nhắc nhở một LLM:
      -> Trường Đại học Carnegie Mellon được thành lập vào năm nào?
    - Những câu hỏi có thể được trả lời tốt hơn bằng cách bổ sung LLM với các tài liệu có liên quan
      -> Tên của lễ hội dưa chua thường niên được tổ chức ở Pittsburgh là gì?
    - Những câu hỏi có khả năng chỉ được trả lời thông qua việc tăng cường
      -> Lễ hội ẩm thực linh hồn Pittsburgh được thành lập khi nào?
    - Các câu hỏi nhạy cảm với tín hiệu thời gian
      -> Ai sẽ biểu diễn tại địa điểm X vào ngày Y?
  - Đối với các câu hỏi có nhiều câu hỏi hợp lệ, bạn có thể đưa ra nhiều câu trả lời trong reference_answers.txt(phân cách bằng dấu chấm phẩy ;). Miễn là hệ thống của bạn tạo ra một trong những câu trả lời hợp lệ, thì câu trả lời đó sẽ được coi là đúng.

Bộ kiểm tra này sẽ cấu thành data/test/questions.txtvà data/test/reference_answers.txttrong bài nộp của bạn .

- Dữ liệu đào tạo: Việc chọn dữ liệu đào tạo linh hoạt hơn 1 chút phụ thuộc vào cách triển khai của bạn. Nếu đang tinh chỉnh mô hình thì có thể:
  - Tự chú thích theo cách thủ công theo phương pháp tưng tự như bộ kiểm tra.
  - Thực hiện một số loại chú thích tự động và/hoặc tăng cường dữ liệu.
  - Sử dụng các tập dữ liệu hiện có để học chuyển giao.
    Nếu bạn đang sử dụng LLM trong môi trường học tập ít nhất 1 lần bạn có thể:
  - Chú thích các ví dụ cho nhiệm vụ bằng phương pháp tương tự như bộ kiểm tra.
  - Sử dụng các tập dữ liệu hiện có để xác định các ví dụ cho việc học theo ngữ cảnh.
- Ước tính chất lượng của tập dữ liệu: Ít nhất 2 thành viên trong nhóm phải chú thích được tập con ngẫu nhiên của tập dữ liệu. Rồi tính toán IAA trên tập dữ liệu này và báo cáo các phát hiện.

###### Phát triển hệ thống RAG của bạn

Hệ thống RAG cần 3 phần sau:

- Trình nhúng tài liệu.
- Trình thu thập tài liệu.
- Trình đọc tài liệu(hay hệ thống trả lời câu hỏi).

Để bắt đầu có thể thử ngăn xếp RAG của langchain sử dụng GPT4All, Chroma và Llama2 cũng như LlamaIndex.

###### Tạo kết quả

Cuối cùng bạn sẽ chạy hệ thống của mình trên bộ kiểm tra của chúng tôi(Chỉ có câu hỏi) và gửi kết quả cho chúng tôi. Bộ kiểm tra này sẽ được phát hành vào ngày trước khi bài tập hết hạn.

###### Bộ kiểm tra chưa thấy

Bạn được phép gửi tối đa ba tệp đầu ra system*outputs/system_output*{1,2,3}.txt chúng tôi sử dụng tệp có hiệu xuất tốt nhất để chấm điểm.

###### Số liệu đánh giá

Bài nộp sẽ được đánh giá dựa trên các số liệu chuẩn, khả năng nhớ lại câu trả lời, độ khớp chính xác và F1.
Xem bài báo cáo của https://arxiv.org/abs/1606.05250 để biết chi tiết. Các số liệu này dựa trên mã thông báo và đo lường sự chồng chéo giữa câu trả lời hệ thống của bạn và câu trả lời tham khảo. Do đó, chúng tôi khuyên bạn nên giữ cho các câu trả lời do hệ thống tạo ra của bạn ngắn gọn nhất có thể.

###### Viết báo cáo

Chúng tôi yêu cầu bạn viết một báo cáo nêu chi tiết các khía cạnh khác nhau về quá trình phát triển hệ thống đầu cuối của bạn (xem tiêu chí chấm điểm bên dưới).

Sẽ có giới hạn 7 trang cho báo cáo và không có mẫu bắt buộc. Tuy nhiên, chúng tôi khuyến khích bạn sử dụng mẫu ACL .

Đảm bảo bạn trích dẫn tất cả các nguồn (mô hình nguồn mở, thư viện, bài báo, blog, v.v.) trong báo cáo của bạn.

###### Nộp bài và chấm điểm

Cấu trúc bài nộp

```
ANDREWID/
├── report.pdf
├── github_url.txt
├── contributions.md
├── data/
│   ├── test/
│   │   ├── questions.txt
│   │   ├── reference_answers.txt
│   ├── train/
│   │   ├── questions.txt
│   │   ├── reference_answers.txt
├── system_outputs/
│   ├── system_output_1.txt
│   ├── system_output_2.txt (optional)
│   ├── system_output_3.txt (optional)
└── README.mdss
```

Phân loại: Các điểm sau đây(tối đa 100 điểm) lấy được từ kết quả và báo cáo của bạn.

- Gửi dữ liệu (15 điểm): gửi dữ liệu thử nghiệm/đào tạo do bạn sáng tạo.
- Gửi mã (15 điểm): gửi mã của bạn để xử lý trước và phát triển mô hình dưới dạng kho GitHub. Chúng tôi có thể không nhất thiết phải chạy mã của bạn, nhưng chúng tôi sẽ xem xét. Vì vậy, hãy đảm bảo rằng nó chứa mã được cập nhật với tệp README nêu rõ các bước để chạy mã. Kho của bạnv.
- Kết quả (30 điểm): điểm dựa trên hiệu suất hệ thống của bạn trên bộ bài kiểm tra riêng của chúng tôi. 10 điểm cho hiệu suất không tầm thường, 5 điểm cộng thêm tối đa 20 điểm dựa trên mức độ hiệu suất so với các bài nộp khác trong lớp.
- Báo cáo : điểm dưới đây sẽ được trao dựa trên báo cáo của bạn.
  - Tạo dữ liệu (10 điểm): mô tả rõ ràng cách bạn tạo dữ liệu của mình. Vui lòng bao gồm các chi tiết sau,
    - Bạn đã biên soạn nguồn kiến ​​thức của mình như thế nào và bạn quyết định đưa những tài liệu nào vào như thế nào?
    - Bạn đã trích xuất dữ liệu thô như thế nào? Bạn đã sử dụng những công cụ nào?
    - Dữ liệu nào được chú thích để thử nghiệm và đào tạo (loại nào và bao nhiêu)?
    - Bạn quyết định loại dữ liệu và lượng dữ liệu cần chú thích như thế nào?
    - Bạn đã sử dụng loại giao diện chú thích nào?
    - Bạn đánh giá chất lượng chú thích của mình như thế nào? (IAA)
    - Đối với dữ liệu đào tạo mà bạn không chú thích, bạn có sử dụng dữ liệu bổ sung nào không và theo cách nào?
  - Chi tiết mô hình (10 điểm): mô tả rõ ràng mô hình của bạn. Vui lòng bao gồm các chi tiết sau,
    - Bạn đã thử những phương pháp nào (bao gồm cả đường cơ sở)? Giải thích ít nhất hai biến thể (nhiều hơn cũng được). Điều này có thể bao gồm mô hình bạn đã sử dụng, dữ liệu nào được đào tạo, chiến lược đào tạo, v.v.
    - Lý do chính đáng nào khiến bạn thử những phương pháp này?
  - Kết quả (10 điểm): báo cáo số liệu thô từ các thí nghiệm của bạn. Vui lòng bao gồm các chi tiết sau,
    - Kết quả của từng mô hình mà bạn thử nghiệm trên dữ liệu thử nghiệm mà bạn tạo ra là gì?
    - Kết quả có ý nghĩa về mặt thống kê không?
  - Phân tích (10 điểm): thực hiện phân tích định lượng/định tính và trình bày các phát hiện của bạn,
    - Thực hiện so sánh các đầu ra ở mức chi tiết hơn là chỉ các con số chính xác toàn diện và báo cáo kết quả. Ví dụ, mô hình của bạn hoạt động như thế nào trên các loại câu hỏi khác nhau?
    - Thực hiện phân tích đánh giá hiệu quả của chiến lược thu thập và bổ sung so với việc sử dụng sổ sách đóng của mô hình.
    - Hiển thị ví dụ về kết quả đầu ra từ ít nhất hai hệ thống bạn đã tạo. Lý tưởng nhất là những ví dụ này có thể đại diện cho những khác biệt về mặt định lượng mà bạn tìm thấy ở trên.

###### Chính sách mô hình và dữ liệu

Làm để cho bài tập có thể tiếp cận được với mọi người

- Bạn chỉ được phép sử dụng các mô hình cũng có thể truy cập thông qua HuggingFace . Điều này có nghĩa là bạn không được sử dụng các mô hình đóng như mô hình OpenAI, nhưng bạn có thể chọn sử dụng dịch vụ lưu trữ cho mô hình mở (như API Hugging Face hoặc Together).
- Bạn chỉ được phép đưa dữ liệu có sẵn công khai vào nguồn kiến ​​thức, dữ liệu thử nghiệm và dữ liệu đào tạo của mình.
- Bạn được phép sử dụng bất kỳ thư viện nguồn mở nào để hỗ trợ chú thích dữ liệu và phát triển mô hình của mình. Hãy đảm bảo bạn kiểm tra giấy phép và ghi rõ nguồn.
