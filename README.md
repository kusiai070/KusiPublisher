# KusiPublisher 🚀

**The AI-Powered Content Creation Platform That Thinks Strategically**

KusiPublisher transforms content creation from a manual, time-consuming process into an intelligent, strategic workflow. Built with 13 specialized AI modules, it combines storytelling expertise, quality assurance, and human touch to create content that truly resonates.

## 🎯 What Makes KusiPublisher Different

Unlike other AI writing tools that just generate text, KusiPublisher:

- **Thinks Strategically**: Uses proven frameworks like StoryBrand SB7, Guber's FEEL/DO, and Salas hooks
- **Ensures Quality**: Built-in quality gates and optimization for every platform
- **Maintains Voice**: Advanced voice analysis to keep your brand consistent
- **Learns & Adapts**: Continuously improves based on your content performance
- **Optimizes for Humans**: Injects authentic human elements that build real connections

## ✨ Key Features

### 🤖 13 AI Modules Working Together

1. **Planning & Approval Workflow** - Strategic content planning with user approval gates
2. **Voice & Style Analyzer** - Maintains brand consistency across all content
3. **Quality & Aesthetics Agent** - Automated quality checks and improvement suggestions
4. **Concepts Panel** - Shows storytelling principles applied to your content
5. **Knowledge Base** - Persistent memory of your preferences and best practices
6. **Platform Agents** - Specialized optimization for LinkedIn, Twitter, Instagram, etc.
7. **SEO & Keyword Research** - Built-in SEO optimization and trend analysis
8. **Human Touch Injector** - Adds authentic, relatable elements
9. **Impact Analyst** - Performance tracking and continuous learning
10. **Visual Generator** - AI-powered visual content suggestions
11. **Strategic Oracle** - High-level content strategy consultation
12. **Interactive Exploration** - Click-to-explore storytelling insights
13. **Version History** - Complete content history with performance metrics

### 🎨 Smart Content Editor

- **Real-time Quality Scoring** - See your content quality improve as you write
- **Platform Previews** - See exactly how your content will look on each platform
- **AI-Powered Suggestions** - Get intelligent recommendations for improvement
- **SEO Optimization** - Built-in keyword research and optimization
- **Visual Suggestions** - AI-generated ideas for supporting visuals

### 📊 Performance Analytics

- **Content Scoring** - Quality metrics across grammar, engagement, SEO, and more
- **Platform Optimization** - Automatic adaptation for each social platform
- **Performance Tracking** - Monitor content success and learn from results
- **Strategic Insights** - High-level recommendations for content strategy

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - Database ORM with SQLite for persistence
- **Multiple AI Providers** - Gemini, OpenAI, Anthropic support
- **Async Processing** - High-performance content generation

### Frontend
- **React 18** - Modern React with hooks and concurrent features
- **Vite** - Lightning-fast build tool and dev server
- **TailwindCSS** - Utility-first styling for rapid development
- **React Router** - Client-side routing for single-page experience

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- API keys from AI providers (Gemini, OpenAI, or Anthropic)

### Installation

1. **Clone and enter the project:**
   ```bash
   cd kusi-publisher
   ```

2. **Run the setup script:**
   ```bash
   ./run.sh
   ```

3. **Configure API keys:**
   - The script will create a `.env` file
   - Add your API keys:
     ```
     GEMINI_API_KEY=your_key_here
     OPENAI_API_KEY=your_key_here
     ANTHROPIC_API_KEY=your_key_here
     ```

4. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

### Manual Installation

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📖 How to Use

### 1. Strategic Planning
- Start with the Planning Workflow to define your content strategy
- Set your objectives, audience, and platforms
- Apply storytelling frameworks (SB7, Guber, Salas)
- Get AI approval at each stage

### 2. Content Creation
- Use the Content Editor for writing and optimization
- Get real-time quality scores and suggestions
- Optimize for specific platforms automatically
- Generate SEO keywords and hashtags

### 3. Quality Assurance
- Let the AI analyze your content for quality
- Get specific improvement recommendations
- Ensure brand voice consistency
- Check platform-specific optimization

### 4. Performance Tracking
- Monitor content performance across platforms
- Learn from successful content patterns
- Get strategic recommendations for improvement
- Build your knowledge base over time

## 🎯 Best Practices

### For Best Results:

1. **Start with Strategy** - Use the planning workflow before creating content
2. **Define Your Voice** - Set up voice profiles for brand consistency
3. **Test Different Approaches** - Use A/B testing features to learn what works
4. **Monitor Performance** - Regularly check the Impact Analyst for insights
5. **Iterate and Improve** - Let the system learn from your successful content

### AI Provider Recommendations:

- **Google Gemini** - Great for content generation and analysis
- **OpenAI GPT** - Excellent for creative writing and brainstorming
- **Anthropic Claude** - Best for strategic thinking and complex analysis

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# AI Provider API Keys
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Active Provider (gemini, openai, anthropic)
ACTIVE_LLM_PROVIDER=gemini

# Database
DATABASE_URL=sqlite:///./kusi_publisher.db

# Application Settings
DEBUG=True
SECRET_KEY=your_secret_key
```

### Customization

- **Voice Profiles**: Train the system on your existing content
- **Brand Guidelines**: Set up your brand voice and style preferences
- **Platform Settings**: Customize optimization for each social platform
- **Quality Thresholds**: Adjust quality scoring to your standards

## 📊 Understanding the Quality Score

KusiPublisher uses a multi-factor quality scoring system:

- **Grammar & Spelling** (25%) - Language correctness
- **Readability** (20%) - Ease of understanding
- **Engagement Potential** (20%) - Likelihood of audience interaction
- **SEO Optimization** (15%) - Search engine friendliness
- **Platform Fit** (10%) - Suitability for target platform
- **Brand Consistency** (10%) - Alignment with voice guidelines

**Score Ranges:**
- 90-100: Excellent - Ready to publish
- 80-89: Good - Minor improvements possible
- 70-79: Fair - Needs significant work
- Below 70: Poor - Major revisions needed

## 🎨 Visual Content Strategy

The Visual Generator provides:

- **Hero Images** - Professional, attention-grabbing visuals
- **Quote Cards** - Typography-focused designs for key messages
- **Infographics** - Data visualization and process diagrams
- **Behind-the-Scenes** - Authentic, personal content
- **Platform-Specific** - Optimized for each social network

## 📈 Performance Tracking

Monitor your content success with:

- **Engagement Metrics** - Likes, comments, shares, clicks
- **Quality Trends** - How your content quality improves over time
- **Platform Performance** - Which platforms work best for your content
- **Voice Consistency** - How well you maintain brand voice
- **ROI Analysis** - Content performance vs. business goals

## 🔒 Privacy & Security

- **Local Data Storage** - All your content and preferences stored locally
- **API Key Security** - Keys stored securely in environment variables
- **No Data Sharing** - Your content and strategies remain private
- **GDPR Compliant** - Built with privacy by design principles

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

Need help? Here are your options:

- **Documentation** - Check the docs folder for detailed guides
- **Issues** - Report bugs or request features on GitHub
- **Community** - Join our Discord for user discussions
- **Email** - Contact support at hello@kusipublisher.com

## 🌟 What's Next

We're constantly improving KusiPublisher:

- **More AI Providers** - Adding support for additional LLM providers
- **Advanced Analytics** - Deeper performance insights and predictions
- **Team Collaboration** - Multi-user features for content teams
- **Integration Hub** - Connect with your favorite marketing tools
- **Mobile App** - Create and manage content on the go

---

**Built with ❤️ by the KusiPublisher Team**

*Transforming content creation through intelligent strategy and authentic storytelling*