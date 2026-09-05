using AiFromMongoAPI.Models;

namespace AiFromMongoAPI.Repositories
{
    public interface ISurveyRepository
    {
        Task<List<Surveys>> GetUsersUsingDocumentationAsync(int limit = 50);
        Task<List<Surveys>> GetUsersUsingDocAndAIAsync(int limit = 50);
        Task<List<Surveys>> GetByAiAccuracyAsync(string aiAcc, int limit = 50);
        Task<List<Surveys>> GetByExperienceLevelAsync(string experienceLevel, int limit = 50);
        Task<List<Surveys>> GetTop20BackEndAiLearnersAsync();
    }
}
