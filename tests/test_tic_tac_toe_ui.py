import pytest
import asyncio
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_create_game():
    async with async_playwright() as p:
        # Запускаем браузер
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Открываем страницу с игрой
        await page.goto('http://127.0.0.1:8000/') 

        # Создаем новую игру
        await page.click('text=Create Game')

        await page.wait_for_timeout(30000)
        #await page.wait_for_url("http://127.0.0.1:8000/game")
        await page.locator('#game-board').wait_for(state='visible')
        game_board = page.locator("#game-board")

        await page.click('text=Copy Game ID')

        await page.wait_for_timeout(2000)

        async def handle_dialog(dialog):
            assert "Game ID copied to clipboard!" in dialog.message, "127.0.0.1:8000"
            await dialog.accept()
        page.on("dialog", handle_dialog)
        
        await page.wait_for_timeout(2000)

        cells = game_board.locator(".cell")
        assert await cells.count()==9, "Игровое поле отображается не корректно!"

        await browser.close()

        # Запуск теста
#asyncio.run(test_create_game())

@pytest.mark.asyncio
async def test_join_game_with_wrong_id():
        
        invalid_know_game_id = "Player2"
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=False)
            context = await browser.new_context()

            page2 = await context.new_page()
            await page2.goto('http://127.0.0.1:8000/')
            await page2.click('text=Invite Player')

            async def handle_dialog(dialog):
                 assert "Enter the Game ID to invite a player:" in dialog.message, "127.0.0.1:8000"
                 await dialog.accept(invalid_know_game_id)

            #await page2.fill('#game-id-input', invalid_know_game_id)

            async def handle_error_dialog(dialog):
                assert "Error inviting player: Game not found" in dialog.message, "127.0.0.1:8000"
                await dialog.accept()
            page2.on("dialog", handle_error_dialog)
            #error_modal = page2.locator("text=Error inviting player: Game not found")
            #await error_modal.wait_for(state="visible", timeout=5000)
            #await page2.click('text=OK')
            #await page2.locator('#game-board').wait_for(state='visible')
            game_board = page2.locator("#game-board")
            await game_board.wait_for(state="visible")
            cells = game_board.locator(".cell")

            assert not await cells.count() == 9, "Игровое поле отображается"

            # Игрок X делает ход в верхний левый угол
            #await page.click('#cell-0')
            #assert await page.inner_text('#cell-0') == 'X', "Ход игрока X не выполнен"

            # Игрок O делает ход в центр
            #await page2.click('#cell-4')
            #assert await page2.inner_text('#cell-4') == 'O', "Ход игрока O не выполнен"

            # Игрок X делает ход в верхний средний
            #await page.click('#cell-1')
            #assert await page.inner_text('#cell-1') == 'X', "Ход игрока X не выполнен"

            # Игрок O делает ход в нижний левый угол
            #await page2.click('#cell-6')
            #assert await page2.inner_text('#cell-6') == 'O', "Ход игрока O не выполнен"

            # Игрок X делает победный ход в верхний правый угол
            #await page.click('#cell-2')
            #assert await page.inner_text('#cell-2') == 'X', "Ход игрока X не выполнен"

            # Проверяем, что игрок X победил
            #winner_message = await page.inner_text('#winner-message')
            #assert 'Player X wins!' in winner_message, f"Ожидалась победа игрока X, но сообщение: {winner_message}"

            # Закрываем браузер
            await browser.close()

# Запуск теста
