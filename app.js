// Telecom Plan Recommendation System JavaScript

// Data from the application
/*const customersData = [
    {"customer_id": "C1", "call_minutes": 1426, "sms_count": 333, "data_gb": 23.12, "roaming_mins": 93, "current_plan": "Plan7", "customer_segment": "Low Usage"},
    {"customer_id": "C2", "call_minutes": 1370, "sms_count": 27, "data_gb": 42.78, "roaming_mins": 61, "current_plan": "Plan1", "customer_segment": "Balanced High Users"},
    {"customer_id": "C3", "call_minutes": 1589, "sms_count": 172, "data_gb": 1.31, "roaming_mins": 114, "current_plan": "Plan4", "customer_segment": "Moderate Users"},
    {"customer_id": "C4", "call_minutes": 1097, "sms_count": 115, "data_gb": 31.22, "roaming_mins": 85, "current_plan": "Plan3", "customer_segment": "Moderate Users"},
    {"customer_id": "C5", "call_minutes": 1916, "sms_count": 177, "data_gb": 1.83, "roaming_mins": 121, "current_plan": "Plan9", "customer_segment": "Moderate Users"},
    {"customer_id": "C49", "call_minutes": 816, "sms_count": 470, "data_gb": 48.28, "roaming_mins": 66, "current_plan": "Plan8", "customer_segment": "Data-Heavy Users"},
    {"customer_id": "C100", "call_minutes": 609, "sms_count": 215, "data_gb": 13.51, "roaming_mins": 122, "current_plan": "Plan1", "customer_segment": "Heavy Voice Users"},
    {"customer_id": "C200", "call_minutes": 1789, "sms_count": 10, "data_gb": 4.33, "roaming_mins": 79, "current_plan": "Plan3", "customer_segment": "Moderate Users"},
    {"customer_id": "C332", "call_minutes": 1692, "sms_count": 148, "data_gb": 49.31, "roaming_mins": 100, "current_plan": "Plan8", "customer_segment": "Balanced High Users"},
    {"customer_id": "C437", "call_minutes": 144, "sms_count": 328, "data_gb": 48.89, "roaming_mins": 28, "current_plan": "Plan8", "customer_segment": "Data-Heavy Users"}
];

const plansData = [
    {"plan_id": "Plan1", "monthly_rental": 299, "free_call_mins": 1905, "free_sms": 303, "free_data_gb": 1, "cost_per_min": 0.72, "cost_per_sms": 0.76, "cost_per_gb": 13},
    {"plan_id": "Plan2", "monthly_rental": 399, "free_call_mins": 150, "free_sms": 340, "free_data_gb": 20, "cost_per_min": 0.37, "cost_per_sms": 0.76, "cost_per_gb": 61},
    {"plan_id": "Plan3", "monthly_rental": 599, "free_call_mins": 498, "free_sms": 93, "free_data_gb": 5, "cost_per_min": 0.39, "cost_per_sms": 0.77, "cost_per_gb": 37},
    {"plan_id": "Plan4", "monthly_rental": 599, "free_call_mins": 399, "free_sms": 69, "free_data_gb": 20, "cost_per_min": 0.23, "cost_per_sms": 0.44, "cost_per_gb": 36},
    {"plan_id": "Plan5", "monthly_rental": 499, "free_call_mins": 1280, "free_sms": 216, "free_data_gb": 5, "cost_per_min": 0.72, "cost_per_sms": 0.67, "cost_per_gb": 39},
    {"plan_id": "Plan6", "monthly_rental": 499, "free_call_mins": 1098, "free_sms": 423, "free_data_gb": 1, "cost_per_min": 0.59, "cost_per_sms": 0.53, "cost_per_gb": 68},
    {"plan_id": "Plan7", "monthly_rental": 499, "free_call_mins": 539, "free_sms": 274, "free_data_gb": 50, "cost_per_min": 0.63, "cost_per_sms": 0.66, "cost_per_gb": 10},
    {"plan_id": "Plan8", "monthly_rental": 499, "free_call_mins": 521, "free_sms": 57, "free_data_gb": 5, "cost_per_min": 0.22, "cost_per_sms": 0.42, "cost_per_gb": 80},
    {"plan_id": "Plan9", "monthly_rental": 499, "free_call_mins": 1127, "free_sms": 366, "free_data_gb": 20, "cost_per_min": 0.37, "cost_per_sms": 0.29, "cost_per_gb": 77},
    {"plan_id": "Plan10", "monthly_rental": 399, "free_call_mins": 224, "free_sms": 476, "free_data_gb": 20, "cost_per_min": 0.47, "cost_per_sms": 0.28, "cost_per_gb": 39}
];
*/
let recommendationsChart = null;
let segmentsChart = null;
let savingsChart = null;


const statistics = {
    "total_customers": 500,
    "customers_who_can_save": 443,
    "average_savings": 744.04,
    "max_savings": 3577.90,
    "average_savings_percentage": 42.42,
    "most_recommended_plans": {"Plan1": 282, "Plan7": 119, "Plan9": 58, "Plan10": 25, "Plan2": 16}
};

const segments = {
    "Moderate Users": {"count": 101, "avg_savings": 571.73, "characteristics": "High voice usage, moderate data"},
    "Heavy Voice Users": {"count": 117, "avg_savings": 331.57, "characteristics": "Focus on calls and SMS"},
    "Low Usage": {"count": 92, "avg_savings": 668.69, "characteristics": "High overall usage across services"},
    "Data-Heavy Users": {"count": 89, "avg_savings": 1012.44, "characteristics": "Primary focus on internet services"},
    "Balanced High Users": {"count": 101, "avg_savings": 1226.27, "characteristics": "Heavy data with moderate voice"}
};

// Cost calculation function
function calculatePlanCost(usage, plan) {
    const roamingCostPerMin = 1.5; // Fixed roaming cost
    let totalCost = plan.monthly_rental;
    
    // Calculate call minutes cost
    const excessCallMins = Math.max(0, usage.call_minutes - plan.free_call_mins);
    totalCost += excessCallMins * plan.cost_per_min;
    
    // Calculate SMS cost
    const excessSMS = Math.max(0, usage.sms_count - plan.free_sms);
    totalCost += excessSMS * plan.cost_per_sms;
    
    // Calculate data cost
    const excessData = Math.max(0, usage.data_gb - plan.free_data_gb);
    totalCost += excessData * plan.cost_per_gb;
    
    // Add roaming cost
    totalCost += usage.roaming_mins * roamingCostPerMin;
    
    return Math.round(totalCost * 100) / 100;
}

// Get recommendations for a customer
function getRecommendations(usage, currentPlan = null) {
    const recommendations = [];
    
    plansData.forEach(plan => {
        const cost = calculatePlanCost(usage, plan);
        recommendations.push({
            plan: plan,
            cost: cost,
            is_current: currentPlan ? plan.plan_id === currentPlan : false
        });
    });
    
    // Sort by cost
    recommendations.sort((a, b) => a.cost - b.cost);
    
    // Calculate savings if there's a current plan
    if (currentPlan) {
        const currentCost = recommendations.find(r => r.is_current)?.cost || 0;
        recommendations.forEach(rec => {
            rec.savings = currentCost - rec.cost;
            rec.savings_percentage = currentCost > 0 ? ((rec.savings / currentCost) * 100) : 0;
        });
    }
    
    return recommendations.slice(0, 3); // Return top 3
}

// Navigation functionality
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.section');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetSection = btn.getAttribute('data-section');
            
            // Update nav buttons
            navButtons.forEach(nb => nb.classList.remove('active'));
            btn.classList.add('active');
            
            // Update sections
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection) {
                    section.classList.add('active');
                }
            });
        });
    });
    
    // Dashboard action buttons
    document.querySelectorAll('[data-action]').forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.getAttribute('data-action');
            const targetBtn = document.querySelector(`[data-section="${action}"]`);
            if (targetBtn) targetBtn.click();
        });
    });
}

// Initialize dashboard statistics
function initDashboard() {
    document.getElementById('total-customers').textContent = statistics.total_customers;
    document.getElementById('customers-can-save').textContent = statistics.customers_who_can_save;
    document.getElementById('avg-savings').textContent = `₹${Math.round(statistics.average_savings)}`;
    document.getElementById('max-savings').textContent = `₹${Math.round(statistics.max_savings).toLocaleString()}`;
}

// Customer lookup functionality
function initCustomerLookup() {
    const lookupBtn = document.getElementById('lookup-btn');
    const customerIdInput = document.getElementById('customer-id');
    const resultsDiv = document.getElementById('customer-results');
    
    lookupBtn.addEventListener('click', () => {
        const customerId = customerIdInput.value.trim().toUpperCase();
        const customer = customersData.find(c => c.customer_id === customerId);
        
        if (customer) {
            displayCustomerResults(customer);
            resultsDiv.classList.remove('hidden');
        } else {
            alert('Customer not found. Try IDs like C1, C2, C3, etc.');
            resultsDiv.classList.add('hidden');
        }
    });
    
    customerIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            lookupBtn.click();
        }
    });
}

// Display customer results
function displayCustomerResults(customer) {
    const detailsDiv = document.getElementById('customer-details');
    const recommendationsDiv = document.getElementById('recommendations-list');
    
    // Display customer details
    detailsDiv.innerHTML = `
        <div class="detail-item">
            <div class="value">${customer.customer_id}</div>
            <div class="label">Customer ID</div>
        </div>
        <div class="detail-item">
            <div class="value">${customer.call_minutes}</div>
            <div class="label">Call Minutes</div>
        </div>
        <div class="detail-item">
            <div class="value">${customer.sms_count}</div>
            <div class="label">SMS Count</div>
        </div>
        <div class="detail-item">
            <div class="value">${customer.data_gb}GB</div>
            <div class="label">Data Usage</div>
        </div>
        <div class="detail-item">
            <div class="value">${customer.roaming_mins}</div>
            <div class="label">Roaming Minutes</div>
        </div>
        <div class="detail-item">
            <div class="value">${customer.current_plan}</div>
            <div class="label">Current Plan</div>
        </div>
        <div class="detail-item">
            <div class="value">${customer.customer_segment}</div>
            <div class="label">Segment</div>
        </div>
    `;
    
    // Get recommendations
    const usage = {
        call_minutes: customer.call_minutes,
        sms_count: customer.sms_count,
        data_gb: customer.data_gb,
        roaming_mins: customer.roaming_mins
    };
    
    const recommendations = getRecommendations(usage, customer.current_plan);
    displayRecommendations(recommendations, recommendationsDiv);
}

// Display recommendations
function displayRecommendations(recommendations, container) {
    container.innerHTML = '';
    
    recommendations.forEach((rec, index) => {
        const isCurrentPlan = rec.is_current;
        const isBest = index === 0 && !isCurrentPlan;
        const savings = rec.savings || 0;
        
        const card = document.createElement('div');
        card.className = `recommendation-card ${isBest ? 'best' : ''}`;
        
        card.innerHTML = `
            ${isBest ? '<div class="recommendation-badge">Best Choice</div>' : ''}
            ${isCurrentPlan ? '<div class="recommendation-badge" style="background: var(--color-info);">Current Plan</div>' : ''}
            <div class="plan-header">
                <div class="plan-name">${rec.plan.plan_id}</div>
                <div class="plan-cost">
                    ${savings > 0 ? `<div class="savings-amount">Save ₹${Math.round(savings)}/month</div>` : ''}
                    <div class="recommended-cost">₹${rec.cost}/month</div>
                </div>
            </div>
            <div class="plan-details">
                <div class="plan-detail">
                    <div class="value">₹${rec.plan.monthly_rental}</div>
                    <div class="label">Base Rental</div>
                </div>
                <div class="plan-detail">
                    <div class="value">${rec.plan.free_call_mins}</div>
                    <div class="label">Free Minutes</div>
                </div>
                <div class="plan-detail">
                    <div class="value">${rec.plan.free_sms}</div>
                    <div class="label">Free SMS</div>
                </div>
                <div class="plan-detail">
                    <div class="value">${rec.plan.free_data_gb}GB</div>
                    <div class="label">Free Data</div>
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
}

// New customer form functionality
function initNewCustomerForm() {
    const ranges = ['call-minutes', 'sms-count', 'data-gb', 'roaming-mins'];
    
    ranges.forEach(id => {
        const range = document.getElementById(id);
        const valueDisplay = document.getElementById(`${id}-value`);
        
        range.addEventListener('input', () => {
            let value = range.value;
            if (id === 'data-gb') {
                value = parseFloat(value).toFixed(1);
            }
            valueDisplay.textContent = value;
            updateNewCustomerRecommendations();
        });
    });
    
    // Initial recommendations
    updateNewCustomerRecommendations();
}

// Update new customer recommendations
function updateNewCustomerRecommendations() {
    const usage = {
        call_minutes: parseInt(document.getElementById('call-minutes').value),
        sms_count: parseInt(document.getElementById('sms-count').value),
        data_gb: parseFloat(document.getElementById('data-gb').value),
        roaming_mins: parseInt(document.getElementById('roaming-mins').value)
    };
    
    const recommendations = getRecommendations(usage);
    const container = document.getElementById('new-recommendations-list');
    displayRecommendations(recommendations, container);
}

// Initialize plans grid
function initPlansGrid() {
    const grid = document.getElementById('plans-grid');
    
    plansData.forEach(plan => {
        const card = document.createElement('div');
        card.className = 'plan-card';
        
        card.innerHTML = `
            <h3>${plan.plan_id}</h3>
            <div class="plan-rental">₹${plan.monthly_rental}/month</div>
            <div class="plan-details">
                <div class="plan-detail">
                    <div class="value">${plan.free_call_mins}</div>
                    <div class="label">Free Minutes</div>
                </div>
                <div class="plan-detail">
                    <div class="value">${plan.free_sms}</div>
                    <div class="label">Free SMS</div>
                </div>
                <div class="plan-detail">
                    <div class="value">${plan.free_data_gb}GB</div>
                    <div class="label">Free Data</div>
                </div>
                <div class="plan-detail">
                    <div class="value">₹${plan.cost_per_min}</div>
                    <div class="label">Per Min</div>
                </div>
                <div class="plan-detail">
                    <div class="value">₹${plan.cost_per_sms}</div>
                    <div class="label">Per SMS</div>
                </div>
                <div class="plan-detail">
                    <div class="value">₹${plan.cost_per_gb}</div>
                    <div class="label">Per GB</div>
                </div>
            </div>
        `;
        
        grid.appendChild(card);
    });
}

// Initialize analytics charts
function initAnalytics() {
    // Most recommended plans chart
    const recCtx = document.getElementById('recommendations-chart').getContext('2d');

    if (recommendationsChart) {
    recommendationsChart.destroy();
    recommendationsChart = null;

  }

    recommendationsChart = new Chart(recCtx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(statistics.most_recommended_plans),
            datasets: [{
                data: Object.values(statistics.most_recommended_plans),
                backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // Customer segments chart
    const segCtx = document.getElementById('segments-chart').getContext('2d');
    if (segmentsChart) {
        segmentsChart.destroy();
        segmentsChart = null;
    }
    segmentsChart  = new Chart(segCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(segments),
            datasets: [{
                label: 'Customers',
                data: Object.values(segments).map(s => s.count),
                backgroundColor: '#1FB8CD',
                borderColor: '#1FB8CD',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Savings by segment chart
    const savingsCtx = document.getElementById('savings-chart').getContext('2d');
    if (savingsChart) {
        savingsChart.destroy();
        savingsChart = null;
    }
    savingsChart = new Chart(savingsCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(segments),
            datasets: [{
                label: 'Average Savings (₹)',
                data: Object.values(segments).map(s => s.avg_savings),
                backgroundColor: '#B4413C',
                borderColor: '#B4413C',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Initialize customer database
function initCustomerDatabase() {
    const tbody = document.getElementById('customers-table-body');
    const segmentFilter = document.getElementById('segment-filter');
    
    function renderCustomerTable(customers = customersData) {
        tbody.innerHTML = '';
        
        customers.forEach(customer => {
            const usage = {
                call_minutes: customer.call_minutes,
                sms_count: customer.sms_count,
                data_gb: customer.data_gb,
                roaming_mins: customer.roaming_mins
            };
            
            const recommendations = getRecommendations(usage, customer.current_plan);
            const bestRecommendation = recommendations[0];
            const savings = bestRecommendation.savings || 0;
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${customer.customer_id}</strong></td>
                <td>${customer.current_plan}</td>
                <td><span class="status status--info">${customer.customer_segment}</span></td>
                <td class="usage-summary">
                    ${customer.call_minutes}min, ${customer.sms_count}SMS, ${customer.data_gb}GB, ${customer.roaming_mins}roam
                </td>
                <td class="savings-highlight">
                    ${savings > 0 ? `₹${Math.round(savings)}/month` : 'No savings'}
                </td>
                <td>
                    <button class="btn btn--sm btn--primary" onclick="lookupCustomer('${customer.customer_id}')">
                        View Details
                    </button>
                </td>
            `;
            
            tbody.appendChild(row);
        });
    }
    
    // Filter functionality
    segmentFilter.addEventListener('change', () => {
        const selectedSegment = segmentFilter.value;
        const filteredCustomers = selectedSegment 
            ? customersData.filter(c => c.customer_segment === selectedSegment)
            : customersData;
        renderCustomerTable(filteredCustomers);
    });
    
    // Initial render
    renderCustomerTable();
}

// Helper function to lookup customer from database
function lookupCustomer(customerId) {
    // Switch to lookup section
    document.querySelector('[data-section="lookup"]').click();
    
    // Fill in the customer ID and trigger lookup
    const customerIdInput = document.getElementById('customer-id');
    customerIdInput.value = customerId;
    document.getElementById('lookup-btn').click();
}

function initializeApp() {
   
    initNavigation();
    initDashboard();
    initCustomerLookup();
    initNewCustomerForm();
    initPlansGrid();
    initAnalytics();
    initCustomerDatabase();

}

let customersData = [];
let plansData = [];

async function loadData() {
  try {
    const customersResponse = await fetch('all_customers.json');
    customersData = await customersResponse.json();

    const plansResponse = await fetch('all_plans.json');
    plansData = await plansResponse.json();

    console.log(`Loaded ${customersData.length} customers and ${plansData.length} plans.`);
    initializeApp(); // Call your app initialization function here after data loads
  } catch (error) {
    console.error('Error loading data:', error);
  }
}


// Call loadData at start
loadData();


// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initDashboard();
    initCustomerLookup();
    initNewCustomerForm();
    initPlansGrid();
    initAnalytics();
    initCustomerDatabase();
});

// Make lookupCustomer available globally
window.lookupCustomer = lookupCustomer;