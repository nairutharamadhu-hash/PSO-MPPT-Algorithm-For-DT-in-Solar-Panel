function dutyCycle = PSO_MPPTracker(PV_voltage, PV_current)

    % PSO Parameters
    numParticles = 30;      % Number of particles in the swarm
    numIterations = 100;    % Number of iterations
    w = 0.5;                % Inertia weight
    c1 = 1.5;               % Cognitive coefficient
    c2 = 1.5;               % Social coefficient

    % Initialize particle positions and velocities
    particlePosition = rand(numParticles, 1) * 0.8; % Duty cycle in range [0, 0.8]
    particleVelocity = rand(numParticles, 1) * 0.1; % Initial velocities
    particleBestPosition = particlePosition;         % Best position for each particle
    particleBestValue = zeros(numParticles, 1);      % Best power value for each particle
    globalBestPosition = particlePosition(1);        % Global best position
    globalBestValue = -inf;                           % Initialize global best value

    % Function to calculate power output based on duty cycle
    calculatePower = @(duty) calculatePVPower(duty, PV_voltage, PV_current);
    
    % PSO Algorithm
    for iter = 1:numIterations
        for i = 1:numParticles
            % Calculate power for each particle's position
            power = calculatePower(particlePosition(i));
            
            % Update personal best
            if power > particleBestValue(i)
                particleBestValue(i) = power;
                particleBestPosition(i) = particlePosition(i);
            end
            
            % Update global best
            if power > globalBestValue
                globalBestValue = power;
                globalBestPosition = particlePosition(i);
            end
        end
        
        % Update particle velocities and positions
        for i = 1:numParticles
            r1 = rand(); % Random value for cognitive component
            r2 = rand(); % Random value for social component
            
            particleVelocity(i) = w * particleVelocity(i) + ...
                                   c1 * r1 * (particleBestPosition(i) - particlePosition(i)) + ...
                                   c2 * r2 * (globalBestPosition - particlePosition(i));
            
            % Update position
            particlePosition(i) = particlePosition(i) + particleVelocity(i);
            
            % Ensure duty cycle is within bounds [0, 1]
            particlePosition(i) = max(0, min(0.8, particlePosition(i))); 
        end
    end
    
    % Output the global best position as duty cycle
    dutyCycle = globalBestPosition;
end

function power = calculatePVPower(duty, voltage, current)
    % Simulate the power output based on duty cycle, voltage, and current
    % Power = voltage * current (for simplicity)
    % In practice, this function can be expanded based on the specific PV model
    power = voltage * current * duty; % Assume the output power is affected by duty cycle
end