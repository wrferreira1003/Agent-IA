import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.agents.main_agent import ChatAgent

@pytest.mark.asyncio
async def test_chat_agent_initialization():
    """Test ChatAgent initialization."""
    with patch('app.agents.main_agent.GeminiModel') as mock_gemini:
        mock_model = Mock()
        mock_chat = Mock()
        mock_model.start_chat.return_value = mock_chat
        mock_gemini.return_value = mock_model
        
        agent = ChatAgent()
        
        assert agent.model_wrapper == mock_model
        assert agent.chat == mock_chat
        mock_model.start_chat.assert_called_once_with(history=None)

@pytest.mark.asyncio
async def test_chat_agent_with_history():
    """Test ChatAgent initialization with history."""
    history = [
        {"role": "user", "parts": ["Hello"]},
        {"role": "model", "parts": ["Hi there!"]}
    ]
    
    with patch('app.agents.main_agent.GeminiModel') as mock_gemini:
        mock_model = Mock()
        mock_chat = Mock()
        mock_model.start_chat.return_value = mock_chat
        mock_gemini.return_value = mock_model
        
        agent = ChatAgent(history=history)
        
        mock_model.start_chat.assert_called_once_with(history=history)

@pytest.mark.asyncio
async def test_get_response_without_function_calls():
    """Test get_response without function calls."""
    with patch('app.agents.main_agent.GeminiModel') as mock_gemini:
        mock_model = Mock()
        mock_chat = Mock()
        mock_response = Mock()
        mock_response.function_calls = None
        mock_response.text = "Simple response"
        mock_chat.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_chat
        mock_gemini.return_value = mock_model
        
        agent = ChatAgent()
        result = await agent.get_response("Hello")
        
        assert result == "Simple response"
        mock_chat.send_message.assert_called_once_with("Hello")

@pytest.mark.asyncio
async def test_get_response_with_function_calls():
    """Test get_response with function calls."""
    with patch('app.agents.main_agent.GeminiModel') as mock_gemini, \
         patch('app.agents.main_agent.available_tools') as mock_tools:
        
        # Setup mocks
        mock_model = Mock()
        mock_chat = Mock()
        mock_function_call = Mock()
        mock_function_call.function.name = "test_function"
        mock_function_call.function.arguments = {"arg1": "value1"}
        
        # First response with function call
        mock_response1 = Mock()
        mock_response1.function_calls = [mock_function_call]
        
        # Second response after function execution
        mock_response2 = Mock()
        mock_response2.text = "Response after function call"
        
        mock_chat.send_message.side_effect = [mock_response1, mock_response2]
        mock_model.start_chat.return_value = mock_chat
        mock_gemini.return_value = mock_model
        
        # Mock tool function
        mock_tool_func = Mock(return_value="Tool result")
        mock_tools.__contains__ = Mock(return_value=True)
        mock_tools.__getitem__ = Mock(return_value=mock_tool_func)
        
        agent = ChatAgent()
        result = await agent.get_response("Execute tool")
        
        assert result == "Response after function call"
        assert mock_chat.send_message.call_count == 2
        mock_tool_func.assert_called_once_with(arg1="value1")