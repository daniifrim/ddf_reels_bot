import os
import requests
import unittest
from unittest.mock import patch, MagicMock
import bot  # Import your main bot file

class TestReelsBot(unittest.TestCase):
    """Test suite for the Instagram Reels Telegram Bot"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a mock Telegram message
        self.mock_message = MagicMock()
        self.mock_message.text = "https://www.instagram.com/reel/ABC123/"
        self.mock_message.from_user.username = "test_user"
        self.mock_message.from_user.first_name = "Test"
        self.mock_message.from_user.id = 12345
        
        # Create a mock bot instance
        self.mock_bot = MagicMock()
        
    def test_instagram_link_regex(self):
        """Test Instagram link regex pattern matching"""
        # Test valid Instagram Reel links
        valid_links = [
            "https://www.instagram.com/reel/ABC123/",
            "https://instagram.com/reel/ABC123",
            "https://www.instagram.com/p/ABC123/",
            "https://instagram.com/p/ABC123/"
        ]
        
        # Test invalid links
        invalid_links = [
            "https://www.instagram.com/stories/username/12345/",
            "https://www.facebook.com/reel/12345",
            "https://example.com",
            "Not a link at all"
        ]
        
        # Check valid links
        for link in valid_links:
            matches = bot.re.findall(bot.INSTAGRAM_REEL_PATTERN, link)
            self.assertTrue(matches, f"Should match valid link: {link}")
            
        # Check invalid links
        for link in invalid_links:
            matches = bot.re.findall(bot.INSTAGRAM_REEL_PATTERN, link)
            self.assertFalse(matches, f"Should not match invalid link: {link}")
    
    @patch('bot.send_to_coda')
    @patch('bot.bot.reply_to')
    def test_handle_message_with_valid_link(self, mock_reply_to, mock_send_to_coda):
        """Test message handler with valid Instagram link"""
        # Configure the mock to return success
        mock_send_to_coda.return_value = (True, 200)
        
        # Call the message handler
        bot.handle_message(self.mock_message)
        
        # Assert that send_to_coda was called with correct parameters
        mock_send_to_coda.assert_called_once_with(
            "https://www.instagram.com/reel/ABC123/", 
            "test_user"
        )
        
        # Assert that reply_to was called with success message
        mock_reply_to.assert_called_once()
        self.assertIn("saved successfully", mock_reply_to.call_args[0][1])
    
    @patch('bot.send_to_coda')
    @patch('bot.bot.reply_to')
    def test_handle_message_with_invalid_link(self, mock_reply_to, mock_send_to_coda):
        """Test message handler with invalid link"""
        # Change the message text to an invalid link
        self.mock_message.text = "https://example.com/not-instagram"
        
        # Call the message handler
        bot.handle_message(self.mock_message)
        
        # Assert that send_to_coda was not called
        mock_send_to_coda.assert_not_called()
        
        # Assert that reply_to was called with error message
        mock_reply_to.assert_called_once()
        self.assertIn("didn't recognize", mock_reply_to.call_args[0][1])
    
    @patch('requests.post')
    def test_send_to_coda_success(self, mock_post):
        """Test sending data to Coda - success case"""
        # Configure the mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Call the function
        success, result = bot.send_to_coda(
            "https://www.instagram.com/reel/ABC123/", 
            "test_user"
        )
        
        # Assert the result
        self.assertTrue(success)
        self.assertEqual(result, 200)
        
        # Assert that requests.post was called with correct parameters
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_send_to_coda_failure(self, mock_post):
        """Test sending data to Coda - failure case"""
        # Configure the mock to raise an exception
        mock_post.side_effect = requests.exceptions.RequestException("API Error")
        
        # Call the function
        success, result = bot.send_to_coda(
            "https://www.instagram.com/reel/ABC123/", 
            "test_user"
        )
        
        # Assert the result
        self.assertFalse(success)
        self.assertIn("Error", result)

if __name__ == '__main__':
    unittest.main() 