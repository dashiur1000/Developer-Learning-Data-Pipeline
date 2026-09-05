using Microsoft.AspNetCore.Mvc;
using AiFromMongoAPI.Repositories;
using AiFromMongoAPI.Models;

namespace AiFromMongoAPI.Controllers
{
    [ApiController]
    [Route("/[controller]")]
    public class SurveysController : ControllerBase
    {
        private readonly ISurveyRepository _repository;
        private readonly ILogger<SurveysController> _logger;
        public SurveysController(ISurveyRepository repository, ILogger<SurveysController> logger)
        {
            _repository = repository;
            _logger = logger;
        }
        [HttpGet("UsingDocumentation")]
        public async Task<ActionResult<IEnumerable<Surveys>>> GetUsersUsingDocumentation([FromQuery] int limit = 50)
        {
            _logger.LogInformation("Getting users using documentation started at {Time}", DateTime.UtcNow);
            var result = await _repository.GetUsersUsingDocumentationAsync(limit);
            _logger.LogInformation("Successfully retrieved {Count} surveys.", result.Count());
            return Ok(result);
        }
        [HttpGet("DocAndAI")]
        public async Task<ActionResult<IEnumerable<Surveys>>> GetUsersUsingDocAnd([FromQuery] int limit = 50)
        {
            _logger.LogInformation("Getting users using documentation started at {Time}", DateTime.UtcNow);
            var result = await _repository.GetUsersUsingDocAndAIAsync(limit);
            _logger.LogInformation("Successfully retrieved {Count} surveys.", result.Count());
            return Ok(result);
        }
        [HttpGet("AiAccuracy/{aiAcc}")]
        public async Task<ActionResult<IEnumerable<Surveys>>> GetByAiAccuracy(string aiAcc, [FromQuery] int limit = 50)
        {
            _logger.LogInformation("Getting users using documentation started at {Time}", DateTime.UtcNow);
            var result = await _repository.GetByAiAccuracyAsync(aiAcc, limit);
            _logger.LogInformation("Successfully retrieved {Count} surveys.", result.Count());
            return Ok(result);
        }
        [HttpGet("ExperienceLevel/{experienceLevel}")]
        public async Task<ActionResult<IEnumerable<Surveys>>> GetByExperienceLevel(string experienceLevel, [FromQuery] int limit = 50)
        {
            _logger.LogInformation("Getting users using documentation started at {Time}", DateTime.UtcNow);
            var result = await _repository.GetByExperienceLevelAsync(experienceLevel, limit);
            _logger.LogInformation("Successfully retrieved {Count} surveys.", result.Count());
            return Ok(result);
        }
        [HttpGet("BackEndAiLearners")]
        public async Task<ActionResult<IEnumerable<Surveys>>> GetTop20BackEndAiLearners()
        {
            _logger.LogInformation("Getting users using documentation started at {Time}", DateTime.UtcNow);
            var result = await _repository.GetTop20BackEndAiLearnersAsync();
            _logger.LogInformation("Successfully retrieved {Count} surveys.", result.Count());
            return Ok(result);
        }
    }
}
