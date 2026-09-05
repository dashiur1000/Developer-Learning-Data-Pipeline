namespace AspConcumer.Models
{
    public class Surveys
    {
        public string ResponseId { get; set; }
        public string? Age { get; set; }
        public int? YearsCode { get; set; }
        public string? DevType { get; set; }
        public string? LearnCodeChoose { get; set; }
        public List<string>? LearnCode { get; set; }
        public string? AILearnHow { get; set; }
        public string? AISelect { get; set; }
        public string? AIAcc { get; set; }
        public string? AISent { get; set; }
        public string? experienceLevel { get; set; }
        public bool? usesDocumentation { get; set; }
        public bool? usesAIForLearning { get; set; }
        public bool? usesStackOverflow { get; set; }
    }
}
