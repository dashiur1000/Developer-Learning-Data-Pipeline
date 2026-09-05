using AiFromMongoAPI.Models;
using MongoDB.Driver;

namespace AiFromMongoAPI.Repositories
{
    public class SurveyRepository : ISurveyRepository
    {
        private readonly IMongoCollection<Surveys> _surveysCollection;

        public SurveyRepository(IMongoCollection<Surveys> collection)
        {
            _surveysCollection = collection;
        }
        public async Task<List<Surveys>> GetUsersUsingDocumentationAsync(int limit = 50) =>
            await _surveysCollection
                .Find(s => s.usesDocumentation == true)
                .Limit(limit)
                .ToListAsync();

        public async Task<List<Surveys>> GetUsersUsingDocAndAIAsync(int limit = 50) =>
            await _surveysCollection.Find(s => s.usesDocumentation == true && s.usesAIForLearning == true).Limit(limit).ToListAsync();

        public async Task<List<Surveys>> GetByAiAccuracyAsync(string aiAcc, int limit = 50) =>
            await _surveysCollection.Find(s => s.AIAcc == aiAcc).Limit(limit).ToListAsync();

        public async Task<List<Surveys>> GetByExperienceLevelAsync(string experienceLevel, int limit = 50) =>
            await _surveysCollection.Find(s => s.experienceLevel == experienceLevel).Limit(limit).ToListAsync();

        public async Task<List<Surveys>> GetTop20BackEndAiLearnersAsync()
        {
            var filter = Builders<Surveys>.Filter.Regex(s => s.DevType, new MongoDB.Bson.BsonRegularExpression("Back-end", "i"));

            return await _surveysCollection
                .Find(filter)
                .Sort(Builders<Surveys>.Sort.Descending(s => s.YearsCode))
                .Limit(20)
                .ToListAsync();
        }
    }
}
