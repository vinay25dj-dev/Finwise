document.addEventListener('DOMContentLoaded', () => {

    // ==== Planner Interaction ====
    const plannerForm = document.getElementById('plannerForm');
    if (plannerForm) {
        // Wizard Stepper Logic
        const steps = Array.from(document.querySelectorAll('.wizard-step'));
        const indicators = Array.from(document.querySelectorAll('.step-indicator'));
        const nextBtns = Array.from(document.querySelectorAll('.next-step'));
        const prevBtns = Array.from(document.querySelectorAll('.prev-step'));
        const progressBar = document.getElementById('wizardProgress');

        let currentStep = 0;

        function updateWizard() {
            steps.forEach((step, index) => {
                step.classList.toggle('active-step', index === currentStep);
                indicators[index].classList.toggle('active', index <= currentStep);
            });
            const progressRaw = ((currentStep + 1) / steps.length) * 100;
            progressBar.style.width = `${progressRaw}%`;
        }

        nextBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // simple validation before next
                const currentInputs = Array.from(steps[currentStep].querySelectorAll('input[required]'));
                const allValid = currentInputs.every(input => input.reportValidity());
                if (allValid && currentStep < steps.length - 1) {
                    currentStep++;
                    updateWizard();
                }
            });
        });

        prevBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                if (currentStep > 0) {
                    currentStep--;
                    updateWizard();
                }
            });
        });

        // Init progress
        updateWizard();

        plannerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const income = parseFloat(document.getElementById('monthly_income').value);
            const expenses = parseFloat(document.getElementById('monthly_expenses').value);
            const savings = parseFloat(document.getElementById('current_savings').value);
            const loan = document.getElementById('loan_amount').value ? parseFloat(document.getElementById('loan_amount').value) : 0;
            const credit_score = document.getElementById('credit_score').value ? parseInt(document.getElementById('credit_score').value) : null;
            const goals = document.getElementById('financial_goals').value;

            const payload = {
                monthly_income: income,
                monthly_expenses: expenses,
                current_savings: savings,
                loan_amount: loan,
                number_of_loans: loan > 0 ? 1 : 0,
                credit_score: credit_score,
                financial_goals: goals
            };

            const btn = document.getElementById('generatePlanBtn');
            const originalText = btn.innerHTML;
            btn.innerHTML = 'Generating ✨...';
            btn.disabled = true;

            try {
                const response = await fetch('/api/planner/plan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) throw new Error('Failed to generate plan');

                const data = await response.json();

                document.getElementById('profileSummary').textContent = data.profile_summary;
                document.getElementById('emergencyAdvice').textContent = data.emergency_fund_advice;

                // Display score
                const scoreEl = document.getElementById('planScore');
                scoreEl.textContent = data.score;
                if (data.score < 40) scoreEl.style.borderColor = '#ef4444';
                else if (data.score < 70) scoreEl.style.borderColor = '#f59e0b';
                else scoreEl.style.borderColor = '#10b981';

                // Render badges
                const badgesCont = document.getElementById('badgesContainer');
                badgesCont.innerHTML = '';
                data.badges.forEach(badge => {
                    const span = document.createElement('span');
                    span.className = 'badge';
                    span.textContent = badge;
                    badgesCont.appendChild(span);
                });

                const strategiesList = document.getElementById('strategiesList');
                strategiesList.innerHTML = '';

                data.strategies.forEach(strategy => {
                    const item = document.createElement('div');
                    item.className = 'strategy-item';

                    const title = document.createElement('h4');
                    title.textContent = strategy.title;

                    const desc = document.createElement('p');
                    desc.textContent = strategy.description;
                    desc.style.color = "var(--text-secondary)";
                    desc.style.marginBottom = "10px";

                    const ul = document.createElement('ul');
                    strategy.action_items.forEach(action => {
                        const li = document.createElement('li');
                        li.textContent = action;
                        ul.appendChild(li);
                    });

                    item.appendChild(title);
                    item.appendChild(desc);
                    item.appendChild(ul);
                    strategiesList.appendChild(item);
                });

                // Initialize Chart.js
                const chartCtx = document.getElementById('cashFlowChart').getContext('2d');
                if (window.cashFlowChartInst) {
                    window.cashFlowChartInst.destroy();
                }

                window.cashFlowChartInst = new Chart(chartCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Monthly Expenses', 'Surplus/Savings'],
                        datasets: [{
                            data: [expenses, Math.max(0, income - expenses)],
                            backgroundColor: ['#ef4444', '#10b981'],
                            borderWidth: 0,
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right',
                                labels: { color: '#f8fafc', font: { family: "'Outfit', sans-serif" } }
                            }
                        }
                    }
                });

                // Hide wizard, show dashboard
                document.getElementById('plannerWizard').style.display = 'none';

                const resultsCont = document.getElementById('resultsContainer');
                resultsCont.style.display = 'block';

            } catch (err) {
                console.error(err);
                alert('We encountered an error setting up your plan.');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        });
    }

    // ==== Game Engine Interaction ====
    let currentGameState = null;
    let currentScenario = null;

    const gameStartBtn = document.getElementById('startGameBtn');
    if (gameStartBtn) {
        gameStartBtn.addEventListener('click', async () => {
            await startNewGame();
        });
    }

    async function startNewGame() {
        try {
            const resp = await fetch('/api/game/start');
            if (!resp.ok) throw new Error('Failed to start game');
            const data = await resp.json();

            document.getElementById('gameStartSect').style.display = 'none';
            document.getElementById('gameActiveSect').style.display = 'block';

            updateGameState(data);
        } catch (err) {
            console.error(err);
            alert('Failed to load game scenario.');
        }
    }

    async function processChoice(choiceObj) {
        if (!currentGameState || !choiceObj) return;

        const payload = {
            state: currentGameState,
            choice: choiceObj
        };

        try {
            const resp = await fetch('/api/game/turn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!resp.ok) throw new Error('Choice processing failed');

            const data = await resp.json();
            updateGameState(data);
        } catch (err) {
            console.error(err);
        }
    }

    function updateGameState(turnResponse) {
        // Find position to spawn animations before updating state
        if (currentGameState && turnResponse.state.balance !== currentGameState.balance) {
            const diff = turnResponse.state.balance - currentGameState.balance;
            spawnFloatingText(diff > 0 ? `+$${diff}` : `-$${Math.abs(diff)}`, diff > 0);
        }

        currentGameState = turnResponse.state;
        currentScenario = turnResponse.next_scenario;

        // Update stats
        document.getElementById('statTurn').textContent = currentGameState.turn_number;
        document.getElementById('statAge').textContent = currentGameState.age;
        document.getElementById('statStage').textContent = currentGameState.life_stage;
        document.getElementById('statTitle').textContent = currentGameState.title;
        document.getElementById('statScore').textContent = currentGameState.score;
        document.getElementById('statBalance').textContent = `$${currentGameState.balance.toLocaleString()}`;
        document.getElementById('statIncome').textContent = `$${currentGameState.monthly_income.toLocaleString()}`;
        document.getElementById('statExpenses').textContent = `$${currentGameState.monthly_expenses.toLocaleString()}`;

        const netFlow = currentGameState.monthly_income - currentGameState.monthly_expenses;
        const statNet = document.getElementById('statNet');
        statNet.textContent = `$${netFlow.toLocaleString()}`;
        statNet.style.color = netFlow >= 0 ? "var(--accent-secondary)" : "#ff4c4c";

        document.getElementById('feedbackMessage').textContent = turnResponse.message;

        // Render scenario
        const titleEl = document.getElementById('scenarioTitle');
        const descEl = document.getElementById('scenarioDesc');
        const choicesContainer = document.getElementById('choicesContainer');

        if (currentScenario) {
            titleEl.textContent = currentScenario.title;
            descEl.textContent = currentScenario.description;
            choicesContainer.innerHTML = '';

            currentScenario.choices.forEach(choice => {
                const btn = document.createElement('button');
                btn.className = 'choice-btn';
                btn.innerHTML = `${choice.text} <span>${choice.impact_description}</span>`;
                btn.addEventListener('click', () => processChoice(choice));
                choicesContainer.appendChild(btn);
            });
        } else {
            titleEl.textContent = "Game Over!";
            descEl.textContent = "You've survived all scenarios. Final Score: " + currentGameState.score;
            choicesContainer.innerHTML = '<button onclick="location.reload()" class="submit-btn" style="width:auto; padding: 10px 30px;">Play Again</button>';
        }
    }

    function spawnFloatingText(text, isPositive) {
        const statsBar = document.querySelector('.stats-bar');
        if (!statsBar) return;

        const el = document.createElement('div');
        el.className = `floating-text ${isPositive ? 'floating-positive' : 'floating-negative'}`;
        el.textContent = text;

        // Randomize slight left/right spawn around center of stats
        const leftOff = 40 + Math.random() * 20;
        el.style.left = `${leftOff}%`;
        el.style.top = `-20px`;

        statsBar.appendChild(el);

        // Clean up DOM after animation (1.5s)
        setTimeout(() => {
            if (el.parentNode) el.parentNode.removeChild(el);
        }, 1500);
    }
});
