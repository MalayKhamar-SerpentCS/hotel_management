

from openerp.osv import osv, fields
from datetime import datetime
import openerp.addons.decimal_precision as dp
from openerp.tools import float_compare

class employee(osv.Model):
    
    _name = 'employee.employee'
    
    def _get_salary(self, cr, uid, ids, fields, args, context=None):
        res = {}
        
        for rec in self.browse(cr, uid, ids, context=context):
            salary = rec.department_id and rec.department_id.salary or 0.0
            res[rec.id] = salary
        return res
    
        
    
    _columns = {
        'name' : fields.char('Name', size=64),
        'age' : fields.integer('Age'),
        'contact_no' : fields.integer('Phone No'),
        'birthdate' : fields.date('Date of Birth'),
        'gender' : fields.selection([('male','Male'), ('female', 'Female')], 'Gender'),
        'is_exp' : fields.boolean('Experienced?'),
        'year_of_exp' : fields.integer('Years of Experience'),
        'notes' : fields.text('Employee Notes'),
        'emp_resume' : fields.binary('Employee Resume'),
        'department_id' : fields.many2one('department.department', 'Department'),
        'emp_signature' : fields.html('Employee Signature'),
        'emp_salary' : fields.function(_get_salary, type="float", string="Salary"),
        'emp_company':fields.many2one('company.company','Company naame'),
    
         
    }
    
class department(osv.Model):
    
    _name = 'department.department'
    
    _rec_name = 'dept_name'
    
   
    _columns = {
        'dept_name' : fields.char('Department Name',size=10),
        'employee_ids' : fields.one2many('employee.employee', 'department_id', 'Employees'),
        'salary' : fields.float('Salary'),
        'currency_id':fields.many2one('res.currency', string='Currency', track_visibility='always'),
    }
    

    def default_get(self,cr,uid,fields,context=None):
        ret_val = super(department, self).default_get(cr,uid,fields,context=context)
        cur_obj = self.pool.get('res.company')
        myid = cur_obj.search(cr,uid,[('name','=','YourCompany')],context=context )
        for rec in cur_obj.browse(cr,uid,myid,context=context):
            curren = rec.currency_id.id
            print'name----------------',rec.currency_id.name
            print'symbol----------------',rec.currency_id.symbol
            ret_val['currency_id'] = curren
            return ret_val
    

class company(osv.Model):
    
    _name = 'company.company'
    
    _columns = {
        'name' : fields.char('Company Name', size=64),
        'department_ids' : fields.many2many('department.department', 'company_department_rel', 
                                            'company_id', 'department_id', 'Departments')
    }